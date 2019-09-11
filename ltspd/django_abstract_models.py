# """Abstract Classes that provide the key inheritance for models
# """
# from django.db import models
# from django.contrib.auth.models import User


# class LtspdCore():
#     """
#     * Name
#     * CreatedBy
#     * CreationDate
#     """
#     name = models.CharField(max_length=100)
#     created_by = models.ForeignKey(User, on_delete=models.CASCADE)
#     creation_date = models.DateTimeField(auto_now=True)


# class LtspdTimeLimited(LtspdCore):
#     """
#     * StartDate
#     * EndDate
#     * Status
#     """
#     start_date = models.DateTimeField(auto_now=True)
#     end_date = models.DateTimeField(auto_now=True)
#     status = models.CharField(max_length=100)


# class LtspdBase(LtspdTimeLimited):
#     """
#     * Category
#     * Description
#     """
#     category = models.CharField(max_length=100)
#     description = models.TextField()


# class LtspdConstruct(LtspdBase):
#     """Abstract Class which contains...

#     * ParticipantFee
#     * Fee
#     * Location
#     * ConstructFields
#     """
#     pass


# class LtspdAddressable():
#     """
#     * CreatedDate
#     * Email
#     * Address
#     * HomeTelephoneNumber
#     * TelephoneNumber
#     * SocialIDs
#     * AuthenticationFields
#     """
#     pass
