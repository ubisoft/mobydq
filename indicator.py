"""Loads indicator configuration files to indicator table."""
import argparse
import configparser
import database
import glob
import logging
import os
import utils


# Load logger
utils.configlogger()
log = logging.getLogger(__name__)


def loadconfiguration(filename=None):
    """Load data quality indicator configuration file into database.

    Configuration files must be placed in folder /indicators
    Configuration files must have the .ini extension
    If no filename is supplied, function will reload all configuration files
    """
    # List indicators configuration files
    currentdirectory = os.path.dirname(os.path.realpath(__file__))
    if filename:
        indicatorfilelist = glob.glob(currentdirectory + '/indicators/' + filename + '.ini')
    else:
        indicatorfilelist = glob.glob(currentdirectory + '/indicators/*.ini')

    # Load files
    parser = configparser.ConfigParser()
    parser.optionxform = str  # Makes parser case sensitive
    for file in indicatorfilelist:
        log.info('Loading configuration file: {}'.format(utils.getfilename(file)))
        parser.read(file)

        # Load indicator attributes
        indicator = parser['INDICATOR']

        # Get indicator type Id
        indicatortype = indicator['indicatorType']
        with database.Function('IndicatorType') as function:
            indicatortypelist = function.read(name=indicatortype)

        if not indicatortypelist:
            log.error('Cannot load indicator file {} because indicator type {} does exist'.format(utils.getfilename(file), indicatortype))
            break

        # Get batch owner Id
        batchowner = indicator['batchOwner']
        with database.Function('BatchOwner') as function:
            batchownerlist = function.read(name=batchowner)

        if not batchownerlist:
            log.error('Cannot load indicator file {} because batch owner {} does exist'.format(utils.getfilename(file), batchowner))
            break

        # Verify if indicator exists
        with database.Function('Indicator') as function:
            indicatorlist = function.read(name=indicator['name'])

        if indicatorlist:
            log.info('Indicator already exists: {}'.format(indicator['name']))
            # Update data quality indicator
            with database.Function('Indicator') as function:
                function.update(
                    id=indicatorlist[0].id,
                    name=indicator['name'],
                    description=indicator['descriptions'],
                    indicatorTypeId=indicatortypelist[0].id,
                    batchOwnerId=batchownerlist[0].id,
                    executionOrder=indicator['executionOrder'],
                    alertOperator=indicator['alertOperator'],
                    alertThreshold=float(indicator['alertThreshold']),
                    distributionList=indicator['distributionList'],
                    active=indicator.getboolean('active'))

        else:
            # Create data quality indicator
            with database.Function('Indicator') as function:
                indicatorlist = function.create(
                    name=indicator['name'],
                    description=indicator['descriptions'],
                    indicatorTypeId=indicatortypelist[0].id,
                    batchOwnerId=batchownerlist[0].id,
                    executionOrder=indicator['executionOrder'],
                    alertOperator=indicator['alertOperator'],
                    alertThreshold=float(indicator['alertThreshold']),
                    distributionList=indicator['distributionList'],
                    active=indicator.getboolean('active'))

        # Load indicator parameters
        indicatorparameter = parser['INDICATOR PARAMETERS']

        for parameter in indicatorparameter:
            # Verify if indicator parameter exists
            with database.Function('IndicatorParameter') as function:
                indicatorparameterlist = function.read(name=parameter, indicatorId=indicatorlist[0].id)

            if indicatorparameterlist:
                with database.Function('IndicatorParameter') as function:
                    function.update(
                        id=indicatorparameterlist[0].id,
                        name=parameter,
                        value=indicatorparameter[parameter],
                        indicatorId=indicatorlist[0].id)

            else:
                with database.Function('IndicatorParameter') as function:
                    function.create(
                        name=parameter,
                        value=indicatorparameter[parameter],
                        indicatorId=indicatorlist[0].id)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '-filename',
        dest='filename',
        type=str,
        help='Enter the name of the data quality indicator configuration file to be loaded in the database, without its extension.')
    arguments = parser.parse_args()
    arguments.filename

    # Call function to load indicator configuration files
    loadconfiguration(arguments.filename)
