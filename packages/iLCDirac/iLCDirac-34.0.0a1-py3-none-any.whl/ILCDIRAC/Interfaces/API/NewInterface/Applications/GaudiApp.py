#
# Copyright (c) 2009-2022 CERN. All rights nots expressly granted are
# reserved.
#
# This file is part of iLCDirac
# (see ilcdirac.cern.ch, contact: ilcdirac-support@cern.ch).
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# In applying this licence, CERN does not waive the privileges and
# immunities granted to it by virtue of its status as an
# Intergovernmental Organization or submit itself to any jurisdiction.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.
#
"""Gaudi Application to run applications based on Gaudi.

.. versionadded:: v32r0p1

Usage:

>>> ga.setVersion('key4hep_nightly')
>>> ga.setExecutable('k4run')
>>> ga.setSteeringFile('geant_fullsim_fccee_lar_pgun.py')
>>> ga.setDetectorModel("DetFCCeeIDEA-LAr")
>>> ga.setArguments("--GenAlg.MomentumRangeParticleGun.MomentumMin 1000 "
>>>                 "--GenAlg.MomentumRangeParticleGun.MomentumMax 1000 "
>>>                 "--GenAlg.MomentumRangeParticleGun.PdgCodes 11")
>>> ga.setOutputFile("output.root")

"""
from __future__ import absolute_import
import types
import os

from ILCDIRAC.Interfaces.API.NewInterface.LCApplication import LCApplication
from ILCDIRAC.Core.Utilities.InstalledFiles import Exists
from ILCDIRAC.Interfaces.Utilities.DDInterfaceMixin import DDInterfaceMixin
from DIRAC import S_OK, S_ERROR, gLogger
from DIRAC.Core.Workflow.Parameter import Parameter
from DIRAC.ConfigurationSystem.Client.Helpers.Operations import Operations
import six

LOG = gLogger.getSubLogger(__name__)
__RCSID__ = "$Id$"


class GaudiApp(DDInterfaceMixin, LCApplication):
  """GaudiApp Application Class."""

  def __init__(self, paramdict=None):
    self.startFrom = 0
    self.randomSeed = -1
    self.detectorModel = ''
    self.executableName = 'k4run'
    self.inputFileFlag = '--EventDataSvc.inputs'
    self.outputFileFlag = '--out.filename'
    self.detectorModelFlag = '--GeoSvc.detectors'
    super(GaudiApp, self).__init__(paramdict)
    # Those 5 need to come after default constructor
    self._modulename = 'GaudiAppModule'
    self._moduledescription = 'Module to run GaudiApp'
    self.appname = 'gaudiapp'
    self._ops = Operations()

  @property
  def detectortype(self):
    """DetectorType needed for transformations.

    Backward compatibility needed for Mokka?
    """
    return self.detectorModel

  @detectortype.setter
  def detectortype(self, value):
    """Ignore setting of detector type for GaudiApp."""
    pass

  def setRandomSeed(self, randomSeed):
    """Define random seed to use. Default is the jobID.

    :param int randomSeed: Seed to use during simulation.
    """
    self._checkArgs({'randomSeed': int})
    self.randomSeed = randomSeed

  def setArguments(self, args):
    """Define the arguments of the script.

    Alternative to :func:`GaudiApp.setExtraCLIArguments`.

    :param str args: Arguments to pass to the command call
    """
    self._checkArgs({'args': (str,)})
    self.extraCLIArguments = args
    return S_OK()

  def setInputFileFlag(self, inputFileFlag):
    """ Optional: Define inputTypeFlag for k4run input files.

    :param str inputFileFlag: type of event files (LCIO, EventDataSvc)
    """
    self._checkArgs({'inputFileFlag': (str,)})
    self.inputFileFlag = inputFileFlag

  def setOutputFileFlag(self, outputFileFlag):
    """Set the command line parameter to be used for setting the output file

    :param str outputFileFlag: prepend flag to ouput file name (e.g. ``--PodioOutput.filename``)
       Default is ``--out.filename``
    """
    self._checkArgs({'outputFileFlag': (str,)})
    self.outputFileFlag = outputFileFlag

  def setDetectorModelFlag(self, detectorModelFlag):
    """Set the command line parameter to be used for setting the detector model file

    :param str detectorModelFlag: prepend flag to detector model file name (e.g. ``--GeoSvc.detectors``)
       Default is ``--GeoSvc.detectors``
    """
    self._checkArgs({'detectorModelFlag': (str,)})
    self.detectorModelFlag = detectorModelFlag

  def setStartFrom(self, startfrom):
    """Define from where GaudiApp starts to read in the input file.

    :param int startfrom: from where GaudiApp starts to read the input file
    """
    self._checkArgs({'startfrom': int})
    self.startFrom = startfrom

  def setExecutable(self, executableName):
    """Set the executable.

    :param str executableName: Name of the gaudi executable program. Default ``k4Run``
    """
    self._checkArgs({'executableName': (str,)})
    self.executableName = executableName

  def _userjobmodules(self, stepdefinition):
    res1 = self._setApplicationModuleAndParameters(stepdefinition)
    res2 = self._setUserJobFinalization(stepdefinition)
    if not res1["OK"] or not res2["OK"]:
      return S_ERROR('userjobmodules failed')
    return S_OK()

  def _prodjobmodules(self, stepdefinition):
    res1 = self._setApplicationModuleAndParameters(stepdefinition)
    res2 = self._setOutputComputeDataList(stepdefinition)
    if not res1["OK"] or not res2["OK"]:
      return S_ERROR('prodjobmodules failed')
    return S_OK()

  def _checkConsistency(self, job=None):
    """Check consistency of the GaudiApp application.

    Called from the `Job` instance.

    :param job: The instance of the job
    :type job: ~ILCDIRAC.Interfaces.API.NewInterface.Job.Job
    :returns: S_OK/S_ERROR
    """
    parameterName = [pN for pN in job.workflow.parameters.getParametersNames() if 'ConfigPackage' in pN]
    configversion = None
    if parameterName:
      LOG.notice("Found config parameter", parameterName)
      config = job.workflow.parameters.find(parameterName[0])
      configversion = config.value
    # Platform must always be defined
    platform = job.workflow.parameters.find("Platform").value

    if not self.version:
      return S_ERROR('No version found')
    if self.steeringFile:
      if not os.path.exists(self.steeringFile) and not self.steeringFile.lower().startswith("lfn:"):
        res = Exists(self.steeringFile, platform=platform, configversion=configversion)
        if not res['OK']:
          return res

    if self._jobtype != 'User':
      self._listofoutput.append({"outputFile": "@{OutputFile}", "outputPath": "@{OutputPath}",
                                 "outputDataSE": '@{OutputSE}'})

      self.prodparameters['detectorType'] = self.detectortype
      self.prodparameters['slic_detectormodel'] = self.detectorModel

    if not self.startFrom:
      LOG.verbose('No startFrom defined for GaudiApp : start from the beginning')

    return S_OK()

  def _applicationModule(self):

    md1 = self._createModuleDefinition()
    md1.addParameter(Parameter("randomSeed", 0, "int", "", "", False, False,
                               "Random seed for the generator"))
    md1.addParameter(Parameter("executableName", "", "string", "", "", False, False,
                               "Name of the executable"))
    md1.addParameter(Parameter("startFrom", 0, "int", "", "", False, False,
                               "From where GaudiApp starts to read the input file"))
    md1.addParameter(Parameter("detectorModel", "", "string", "", "", False, False,
                               "Detecor model for simulation"))
    md1.addParameter(Parameter("inputFileFlag", "", "string", "", "", False, False,
                               "Flag that define the type flag for input files (lcio, eventdatasvc, ..)"))
    md1.addParameter(Parameter("outputFileFlag", "", "string", "", "", False, False,
                               "Flag that defines the output file flag (e.g. PodioOutput)"))
    md1.addParameter(Parameter("detectorModelFlag", "", "string", "", "", False, False,
                               "Flag that defines the detector model file flag (e.g. GeoSvc)"))
    md1.addParameter(Parameter("debug", False, "bool", "", "", False, False, "debug mode"))
    return md1

  def _applicationModuleValues(self, moduleinstance):

    moduleinstance.setValue("randomSeed", self.randomSeed)
    moduleinstance.setValue("executableName", self.executableName)
    moduleinstance.setValue("startFrom", self.startFrom)
    moduleinstance.setValue("detectorModel", self.detectorModel)
    moduleinstance.setValue("inputFileFlag", self.inputFileFlag)
    moduleinstance.setValue("outputFileFlag", self.outputFileFlag)
    moduleinstance.setValue("detectorModelFlag", self.detectorModelFlag)
    moduleinstance.setValue("debug", self.debug)

  def _checkWorkflowConsistency(self):
    return self._checkRequiredApp()

  def _resolveLinkedStepParameters(self, stepinstance):
    if isinstance(self._linkedidx, six.integer_types):
      self._inputappstep = self._jobsteps[self._linkedidx]
    if self._inputappstep:
      stepinstance.setLink("InputFile", self._inputappstep.getType(), "OutputFile")
    return S_OK()
