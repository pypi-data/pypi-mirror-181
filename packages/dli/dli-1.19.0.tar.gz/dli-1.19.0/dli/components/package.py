#
# Copyright (C) 2020 IHS Markit.
# All Rights Reserved
#
import logging
import warnings
from deprecated import deprecated
from platform_services_lib.lib.aspects.base_component import BaseComponent

logger = logging.getLogger(__name__)


class Package(BaseComponent):

    _KNOWN_FIELDS = {"name",
                     "description",
                     "keywords",
                     "topic",
                     "access",
                     "internalData",
                     "contractIds",
                     "termsAndConditions",
                     "derivedDataNotes",
                     "derivedDataRights",
                     "distributionNotes",
                     "distributionRights",
                     "internalUsageNotes",
                     "internalUsageRights",
                     "documentation",
                     "publisher",
                     "techDataOpsId",
                     "accessManagerId",
                     "managerId",
                     "intendedPurpose",
                     "isInternalWithinOrganisation"}
    """
    A mixin providing common package operations
    """

    @classmethod
    @deprecated(reason="Registration of packages has now moved out of the SDK's remit", version="1.18.0")
    def get_default_package_terms_and_conditions(cls, organisation_name: str):
        """
        Returns a string representing the default Terms And Conditions for packages created in DataLake for a given organisation.

        :Example:

            .. code:: python

                client.get_default_package_terms_and_conditions('IHSMarkit')

        :returns: The default DataLake Terms And Conditions
        :rtype: str
        """
        # Scott: please do not deprecate this function. It is used by Excel users.
        # TR 2022-04-11 - we are now S&P Global, we should not have an IHS Markit specific method stapled to the SDK.
        # It's also only applying to IHS Markit or an empty string in use.
        # The funniest reason is, that this method is used in registering a package with default T&Cs
        # -- a method `register_package` which was removed months before this function.

        if organisation_name == 'IHS Markit':
            return ('By submitting this Data request and checking the "Accept Terms and Conditions" '
                'box, you acknowledge and agree to the following:\n'
                '\n'
                '* To promptly notify the relevant Access Manager/Producer of your intended use '
                'of the Data;\n'
                '* To obtain the terms and conditions relevant to such use for such Data from '
                'the Producer;\n'
                '* To distribute such terms and conditions to each member of your '
                'Consumer Group who may use the Data;\n'
                '* To use the Data solely for such intended use, subject to such terms and '
                'conditions;\n'
                '* To ensure that the Data is only accessed by members of your Consumer Group, '
                'and only used by such members for such intended use, subject to such terms and '
                'conditions;\n'
                '* To adhere to any additional requests of Producer with respect to the Data '
                '(including but not limited to ceasing use of the Data and deleting the Data, '
                'and ensuring other members of the Consumer Group do so, upon revocation of your '
                'license by Producer).\n'
                '\n'
                'Please refer to the <a href="/terms-of-use" target="_blank">EULA</a> for any '
                'defined terms used above. '
                'The <a href="/terms-of-use" target="_blank">EULA</a> '
                'is the document you agreed to adhere to by accessing the Lake.')
        else:
            return ''
