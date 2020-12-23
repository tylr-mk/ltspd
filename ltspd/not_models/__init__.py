"""Abstract Classes that provide the key inheritance for models
"""


class LtspdCore:
    """
    * Name
    * CreatedBy
    * CreatedDate
    """

    pass


class LtspdTimeLimited(LtspdCore):
    """
    * StartDate
    * EndDate
    * Status
    """

    pass


class LtspdBase(LtspdTimeLimited):
    """
    * Type
    * Description
    """

    pass


class LtspdConstruct(LtspdBase):
    """Abstract Class which contains...

    * ParticipantFee
    * Fee
    * Location
    * ConstructFields
    """

    pass


class LtspdAddressable:
    """
    * CreatedDate
    * Email
    * Address
    * HomeTelephoneNumber
    * TelephoneNumber
    * SocialIDs
    * AuthenticationFields
    """

    pass
