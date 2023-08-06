"""
Experiment trackers for machine learning pipelines.
"""
import os
from abc import ABC, abstractmethod

import neptune.new as neptune
import neptune.new.integrations.sklearn as npt_utils
from neptune.new.types import File
import wandb
from io import BytesIO, StringIO
import pandas as pd
from plotly.io import to_html

# typing
from numpy import ndarray
from pandas import DataFrame
from typing import Union, List
from matplotlib.figure import Figure
from plotly.graph_objs._figure import Figure as PlotlyFigure

# TODO: implementation-specific documentation


class ExperimentTracker(ABC):
    """
    Encapsulates metadata for experiment tracking across runs.
    """

    @abstractmethod
    def __init__(self, projectID: str, entityID: str, analysisName: str, **kwargs):

        self.entityID = entityID
        self.projectID = projectID
        self.analysisName = analysisName

    def start(self, **kwargs):
        """
        Initialize tracker with a given model.
        """

    def summarize(self, **kwargs):
        """
        Generate classifier summary.
        """

    def log(self, **kwargs):
        """
        Log a value to track.
        """

    def addTags(self, **kwargs):
        """
        Append tags to the current tracking run.
        """

    def getRuns(self, **kwargs):
        """
        Fetch the latest runs by ID or tag. All runs are fetched by default.
        """

    def stop(self, **kwargs):
        """
        Send halt signal to experiment tracker and avoid memory leaks.
        """


class NeptuneExperimentTracker(ExperimentTracker):
    """
    Interface for experiment tracking using Neptune.
    """

    def __init__(self, projectID: str, entityID: str, analysisName: str, **kwargs):
        super().__init__(projectID, entityID, analysisName, **kwargs)

        self.apiToken = kwargs["apiToken"]

    def loadProject(self):
        self.project = neptune.init_project(
            name=self.entityID + "/" + self.projectID, api_token=self.apiToken
        )

    def start(self, model):
        self.tracker = neptune.init(
            project=self.entityID + "/" + self.projectID,
            api_token=self.apiToken,
            name=self.analysisName,
            capture_hardware_metrics=False,
        )
        self.addTags([model.__class__.__name__])
        self.model = model

        # Neptune bug workaround: cache IO streams to disk (https://github.com/neptune-ai/neptune-client/issues/889)
        # self.tempDir = os.path.join(os.getcwd(), ".neptune/temp")
        # if not os.path.exists(self.tempDir):
        #     os.makedirs(self.tempDir)

    def summarize(
        self,
        model,
        trainingData: ndarray,
        testingData: ndarray,
        trainingLabels: ndarray,
        testingLabels: ndarray,
        **kwargs,
    ):
        self.tracker["summary"] = npt_utils.create_classifier_summary(
            model, trainingData, testingData, trainingLabels, testingLabels
        )

    def log(
        self,
        path: str,
        valueMap: dict,
        projectLevel=False,
        **kwargs,
    ):
        loggable = self.project if projectLevel else self.tracker

        for (key, value) in valueMap.items():
            if isinstance(value, Figure):
                fileHandle, previewHandle = BytesIO(), BytesIO()
                value.savefig(fileHandle, format="svg", bbox_inches="tight")
                loggable[f"{path}/{key}"].upload(
                    File.from_stream(fileHandle, extension="svg")
                )
                value.savefig(previewHandle, format="png", bbox_inches="tight")
                loggable[f"{path}/{key} preview"].upload(
                    File.from_stream(previewHandle, extension="png")
                )
            elif isinstance(value, PlotlyFigure):
                loggable[f"{path}/{key}"].upload(
                    File.from_content(to_html(value), extension="html")
                )
            elif isinstance(value, DataFrame):
                tableStream = BytesIO()
                value.to_csv(tableStream, header=True, index=True)
                loggable[f"{path}/{key}"].upload(
                    File.from_stream(tableStream, extension="csv")
                )
            elif key == "model":
                loggable[f"{path}/{key}"].upload(
                    File.from_stream(BytesIO(value), extension="pkl")
                )
            elif isinstance(value, BytesIO) or isinstance(value, StringIO):
                loggable[f"{path}/{key}"].upload(File.from_stream(value))
            else:
                loggable[f"{path}/{key}"] = value

    def addTags(self, tags: List):
        self.tracker["sys/tags"].add(tags)

    def getRuns(
        self,
        runID: Union[List, str] = None,
        tag: Union[List, str] = None,
    ):
        project = neptune.get_project(name=self.projectID, api_token=self.apiToken)
        self.runs = project.fetch_runs_table(id=runID, tag=tag)

    def stop(self):
        self.tracker.stop()


os.environ["WANDB_START_METHOD"] = "thread"


class WandbExperimentTracker(ExperimentTracker):
    """
    Interface for experiment tracking using Weights & Biases.
    """

    def __init__(self, projectID: str, entityID: str, **kwargs):
        super().__init__(projectID, entityID, **kwargs)

        if kwargs["threaded"]:
            self.threaded = True
        self.api = wandb.Api()

    def start(self, model, type="sklearn"):
        self.tracker = wandb.init(
            project=self.projectID,
            entity=self.entityID,
            reinit=True,
            settings=wandb.Settings(
                start_method=("thread" if self.threaded else "fork")
            ),
        )
        if type != "sklearn":
            self.tracker.watch(model)
        self.tracker.name = model.__class__.__name__

    def summarize(
        self,
        model,
        hyperparameters: dict,
        trainingData: DataFrame,
        testingData: DataFrame,
        trainingLabels: ndarray,
        testingLabels: ndarray,
        testPredictions: ndarray,
        testProbabilities: ndarray,
        classLabels: List[str] = None,
        featureLabels: List[str] = None,
        isSklearn: bool = True,
    ):
        self.tracker.config.update(hyperparameters)
        if isSklearn:
            wandb.sklearn.plot_classifier(
                model=model,
                X_train=trainingData,
                X_test=testingData,
                y_train=trainingLabels,
                y_test=testingLabels,
                y_pred=testPredictions,
                y_probas=testProbabilities,
                labels=classLabels,
                model_name=model.__class__.__name__,
                feature_names=featureLabels,
            )

    def log(self, path: str, valueMap: dict, step: int = None):
        runningLog = dict()
        for (key, value) in valueMap.items():
            if isinstance(value, Figure):
                value.tight_layout()
                svgHandle = StringIO()
                value.savefig(svgHandle, format="svg", bbox_inches="tight")
                runningLog[key] = wandb.Html(svgHandle)
                runningLog[key + " preview"] = wandb.Image(value)
            elif isinstance(value, DataFrame):
                runningLog[key] = wandb.Table(dataframe=value.reset_index())
            else:
                runningLog[key] = value
        self.tracker.log({path: runningLog}, step=step)

    def addTags(self, tags: List):
        self.tracker.tags.append(tags)

    def getRuns(self):
        self.runs = self.api.runs(self.entityID + "/" + self.projectID)

    def stop(self):
        self.tracker.finish()
