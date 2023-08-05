# telus-bulk-types-pypi

## Import models using

    from telus_bulk.models

## E.g
    from telus_bulk.models.worker_job import AddressProcessingJob
    job_data: AddressProcessingJob = AddressProcessingJob.parse_raw(message.data)

## PYTEST
The .env file must have the PYTHONPATH variable  

    PYTHONPATH=src

# Changelog

1.2.9
- Added optional 'customerName' field to models/tmf_645/related_party.py

1.2.8
- Added ThreadJob class to be a helper for Oauth access token fetch

1.2.6
- City Alias Class and field in PlaceAMS added

1.2.6
- modified province attribute and added cityCoverage for related party 

1.2.4
- add province capability to related party for tmf-632 organizations short response

1.2.2:
- Reports models updated using new clli implementation

1.2.1:
- CLLI: model updated

1.2.0:
- Reports full support

1.1.19:
- ReportsAddressUpdateDto and Reports default value updated

1.1.18:
- ReportsAddressUpdateDto

1.1.17:
- Reports CamelCase models with tests

1.1.16:
- checkServiceQualificationCreate.relatedParty added default value (SFDC)

1.1.15:
- Clli model added
- CheckServiceQualificationItem.place.clli added 

1.1.14:
- CheckServiceQualificationItem.expiration_date added pre validator to parse to datetime

1.1.12:
- http_post set default content_type to "FORM-ENCODED" for backward compatibility
- createdAt in models Union["Any"]

1.1.12:
- Typo: Overall file updated names

1.1.11:
- 
- OverallProcessorType created, OverAllData updated [field created: processor_type ]
- ServiceEligibilityUnavailabilityReason  [Field created: construction_charge, comments]
- Httpx helper class post with application/json support

1.1.9:
- CheckServiceQualification and CheckServiceQualificationItem models updated with createdAt field
- OverAllProcessStatus, OverAllProcess, OverAllData classes created

1.1.8:
- Pagination model validated for page to always be greater than 1  
- CheckServiceQualificationItem:  
        effective_qualification_item_date  create as str  
        expiration_date updated from datetime to str  
- ServiceRefOrValue  
    service_specification updated to Union of List[ServiceSpecificationRef] | List[ServiceSpecification]

1.1.6:
- PageDto paginationMetadata -> meta

1.1.6:
- Added pagination models and pytest

1.1.5:
- Added RelatedParty class to CityCoverageProcessedJob.relatedParty, instead of a string array
- WebMethods init module updated to export get and post methods
- 645/service/place updated priority to match first PlaceAMS class

1.1.3:
- Added Web Methods

1.1.0:
- Added more AMS fields to PlaceAMS, First demo ready!

1.0.7:
- Added more AMS fields to PlaceAMS

1.0.6:
- Partner list bug fix

1.0.5:
- Added supported partners enum and list  

1.0.3:
- Optional AMS Coordinates object fields, except for latitude and longitude

1.0.2:
- Added CityCoverageProcessedJob class
- CSQI service supports a PlaceAms as Place