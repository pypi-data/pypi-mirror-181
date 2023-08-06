"""
Contains a data mediator to split, balance, and holdout experimental
and control data for machine learning pipelines.
"""

from typing import Callable, Optional, Union, List
import pandas as pd
from pandas import DataFrame
import numpy as np
from sklearn.model_selection import train_test_split


class DataMediator:
    """
    Split & balance a dataframe with shape (sample, variables) into `experimental`
    and `control` class variables.

    TODO: Filtering may be done with a user-defined mapping of conditions to columns.

    [Args]
        `dataframe` (DataFrame): Data to split, balance, and take holdout \n
        `testProportion` (float): Percentage of data from experimental & control sets to holdout. \n
        `controlIDs` (list[str]): List of sample IDs in the control set. \n
        `experimentalIDs` (list[str]): List of sample IDs in the experimental set. \n
        `randomSeed` (int): Seed number to replicate psuedorandom sampling.

    [Optional]
        `holdoutProportion` (float): Percentage of data from experimental & control sets to holdout. \n
        `balancingMethod` (str): Sampling method used for data balancing. The default is "downsampling"; "upsampling" or "smote" are additional options. Sampling occurs via the Pandas `sample()` method, unless another callback is defined. \n
        `balancingMethodCallback` (Callable): A custom sampling method callback, which is called instead of Pandas sample() on control, experimental & holdout dataframes. \n
        `filterMap`: TODO \n
        `verbose` (bool): Flag that determines whether DataMediator logs activity to STDOUT. \n
    """

    def __init__(
        self,
        dataframe: DataFrame,
        testProportion: float,
        controlIDs: list,
        experimentalIDs: list,
        randomSeed: int,
        balancingMethod: str = "downsampling",
        **kwargs,
    ) -> None:
        self.dataframe = dataframe
        self.testProportion = testProportion
        self.randomSeed = randomSeed
        self.balancingMethod = balancingMethod

        # split experimental & control data with given IDs
        self.experimental = self.__splitDataFrame(experimentalIDs)
        self.control = self.__splitDataFrame(controlIDs)

        # record initial state of dataframes
        self.__experimental = self.experimental.copy(deep=True)
        self.__control = self.control.copy(deep=True)
        self.originalExperimentalIDs = self.__experimental.index.tolist()
        self.originalControlIDs = self.__control.index.tolist()

        # set flags
        # take holdouts before any data balancing
        if "holdoutProportion" in kwargs:
            self.holdoutProportion = kwargs["holdoutProportion"]
            del kwargs["holdoutProportion"]
        self.balancingMethodCallback = None
        for flag, value in kwargs.items():
            # TODO: refactor using match case upon python 3.10 release
            # balance with given sampling method
            if flag == "balancingMethodCallback":
                self.balancingMethodCallback = value
            if flag == "filterMap":
                self.filter(value)
            if flag == "verbose":
                self.verbose = value
        if balancingMethod:
            self.__balance(self.balancingMethodCallback)

    @staticmethod
    def transposeDataFrame(
        dataframe,
        columnToTranspose: str,
        columnsToDrop: Union[List[str], slice] = [],
    ) -> DataFrame:
        """
        Static method to transpose a dataframe by a given column,
        with a new row index.
        """

        # drop transposed column IDs from data
        transposed = dataframe.drop(
            columns=(
                dataframe.columns[columnsToDrop]
                if type(columnsToDrop) == slice
                else columnsToDrop
            )
        ).T.iloc[1:, :]
        columnIDs = dataframe[columnToTranspose].tolist()

        # set new indices
        transposed.columns = columnIDs

        return transposed

    @staticmethod
    def filter(
        dataframe,
        column,
        lowerBound: Union[int, float] = None,
        upperBound: Union[int, float] = None,
        proportion: float = None,
        metric: bool = True,
    ) -> DataFrame:
        """
        Filter rows of a given dataframe by column and condition. Numerical values may be taken by upper
        and lower bounds, or by proportion and a single bounding criterion.
        """
        if metric:
            if upperBound and lowerBound:
                return dataframe.loc[
                    (dataframe[column] >= lowerBound)
                    & (dataframe[column] <= upperBound)
                ]
            elif proportion and (upperBound or lowerBound):
                return (
                    dataframe.sort_values(
                        by=column,
                        axis=0,
                        ascending=True if lowerBound else False,
                    )
                    .iloc[: -int(len(dataframe) * proportion)]
                    .sort_index()
                )

    @staticmethod
    def removeNullColumns(dataframe) -> DataFrame:
        """
        Drop columns with all zero, NaN or null values.
        """
        # check if any truthy values exist per column
        nullColumnView = dataframe.any()

        return dataframe.loc[:, nullColumnView]

    def __splitDataFrame(self, IDs: list) -> DataFrame:
        """
        Private method to excise a list of desired sample IDs from the
        dataframe attached to this instance, into experimental
        & control dataframes.
        """
        import logging

        missingIDs = []
        for ID in IDs:
            if ID not in self.dataframe.index:
                missingIDs.append(ID)
        if len(missingIDs) >= 1:
            logging.warning(f"samples missing from feature data: {missingIDs}")
        return self.dataframe.loc[[ID for ID in IDs if ID in self.dataframe.index]]

    def __balance(
        self,
        balancingMethodCallback: Optional[Callable] = None,
    ) -> None:
        """
        Private method to balance control, experimental & holdout datasets, with a
        given sampling method. The default is "downsampling"; "upsampling" or "smote"
        are additional options. A custom sampling method callback may also be passed,
        which is called instead on split & holdout dataframes.
        """
        largeSplit = max([self.experimental, self.control], key=len)
        smallSplit = min([self.experimental, self.control], key=len)

        if hasattr(self, "verbose"):
            print(f"Unbalanced classes— {False if largeSplit == smallSplit else True}")
            print(f"Minority split count: {len(largeSplit)}")
            print(f"Majority split count: {len(smallSplit)}")

        # Balancing the Data
        # ignore chained assigment warning in Pandas since we are dropping rows in-place
        pd.options.mode.chained_assignment = None
        if balancingMethodCallback and self.balancingMethod == "downsampling":
            dataToKeep = balancingMethodCallback(largeSplit)
            largeSplit.drop(
                dataToKeep.index.symmetric_difference(largeSplit.index), inplace=True
            )
        elif balancingMethodCallback and self.balancingMethod == "upsampling":
            dataToAdd = balancingMethodCallback(smallSplit)
            smallSplit.merge(dataToAdd)
        elif self.balancingMethod == "downsampling":
            dataToKeep = largeSplit.sample(
                len(smallSplit), random_state=self.randomSeed
            )
            largeSplit.drop(
                dataToKeep.index.symmetric_difference(largeSplit.index), inplace=True
            )
        elif self.balancingMethod == "upsampling":
            dataToAdd = smallSplit.sample(
                len(largeSplit), replace=True, random_state=self.randomSeed
            )
            smallSplit.merge(dataToAdd)
        # restore chained assignment warning
        pd.options.mode.chained_assignment = "warn"

    @property
    def featureCount(self, columnStratified=True):
        """
        Return number of features from the input dataframe. If features are
        stratified by row, set `columnStratified` to falsy.
        """
        if hasattr(self, "train") and hasattr(self, "validation"):
            trainingShape = self.train.shape[1 if columnStratified else 0]
            testingShape = self.validation.shape[1 if columnStratified else 0]
            return (
                testingShape
                if testingShape == trainingShape
                else "unmatched feature count between training & testing!"
            )
        elif hasattr(self, "experimental") and hasattr(self, "control"):
            experimentalShape = self.experimental.shape[1 if columnStratified else 0]
            controlShape = self.control.shape[1 if columnStratified else 0]
            return (
                controlShape
                if controlShape == experimentalShape
                else "unmatched feature count between cases & controls!"
            )
        else:
            return self.dataframe.shape[1 if columnStratified else 0]

    def resample(self, keepFilters=False) -> None:
        """
        Reinitialize experimental & control data; redo dataset balancing.
        """
        if not keepFilters:
            self.experimental = self.__experimental.copy(deep=True)
            self.control = self.__control.copy(deep=True)
        if self.balancingMethod:
            self.__balance(self.balancingMethodCallback)
        self.trainTestSplit()

    def trainTestSplit(self, stratifyByClass=True, samplingSpace="internal") -> None:
        """
        Split control (class 0) and experimental data (class 1) by a given proportion into training/validation sets.
        Also takes independent holdout if `holdoutProportion` was passed during initialization.

        [Input]
            `stratifyByClass`: stratify class proportions when splitting \n
        [New attributes]
            `train` \n
            `trainLabels` \n
            `validation` \n
            `validationLabels` \n
            `holdout` \n
            `holdoutLabels` \n
            `featureIndex` \n
        """
        allData = pd.concat([self.control, self.experimental])
        allLabels = np.array([0] * len(self.control) + [1] * len(self.experimental))

        self.featureIndex = allData.index.tolist()

        if samplingSpace == "external":
            testProportion = self.testProportion
            (
                self.holdout,
                self.validation,
                self.holdoutLabels,
                self.validationLabels,
            ) = train_test_split(
                allData.astype(int),
                allLabels,
                test_size=testProportion,  # percentage if less than 1
                stratify=allLabels if stratifyByClass else None,
                random_state=self.randomSeed,
            )
        elif self.holdoutProportion:
            # calculate number of samples in validation group
            testProportion = int(self.testProportion * len(allData))
            (
                postHoldoutData,
                self.holdout,
                postHoldoutLabels,
                self.holdoutLabels,
            ) = train_test_split(
                allData.astype(int),
                allLabels,
                test_size=self.holdoutProportion,
                stratify=allLabels if stratifyByClass else None,
                random_state=self.randomSeed,
            )
            (
                self.train,
                self.validation,
                self.trainLabels,
                self.validationLabels,
            ) = train_test_split(
                postHoldoutData.astype(int),
                postHoldoutLabels,
                test_size=testProportion,  # percentage if less than 1
                stratify=postHoldoutLabels if stratifyByClass else None,
                random_state=self.randomSeed,
            )
        else:
            testProportion = self.testProportion
            (
                self.train,
                self.validation,
                self.trainLabels,
                self.validationLabels,
            ) = train_test_split(
                allData.astype(int),
                allLabels,
                test_size=testProportion,  # percentage if less than 1
                stratify=postHoldoutLabels if stratifyByClass else None,
                random_state=self.randomSeed,
            )

    def loadPredictions(self, probabilities: list, dataGroup: str):
        """
        Index an array-like of numeric predictions into a dataframe. Training & testing
        data must be split before using this method.

        [Input]
            `testData`: Boolean to indicate whether predictions are obtained from training or testing.

        [New attributes]
            `predictions`
        """
        self.predictions = pd.DataFrame(
            {
                "y_true": self.validationLabels
                if dataGroup == "validation"
                else self.trainLabels
                if dataGroup == "train"
                else self.holdoutLabels,
                "y_pred": np.argmax(probabilities, axis=1),
                "y_probas": list(probabilities),
            }
        )
