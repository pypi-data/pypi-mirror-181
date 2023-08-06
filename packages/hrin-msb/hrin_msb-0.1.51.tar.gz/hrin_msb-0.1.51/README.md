# hrin-msb

## Pre-requisites for setup
1. `pip install poetry`

## How To Build

1. `poetry build`
2. `poetry config http-basic.pypi __token__ <access-token>`
3. `poetry publish`


# Change Log
 ### Version 0.1.1
***

 ### Version 0.1.2
***

 ### Version 0.1.3
***

1.  Default serializer added to ApiView
2. fixed incorrect import in _validators.py
3. fixed msb_database_router
4. fixed Config.is_local_env() not working
5. moved devscripts -> devtools
6. File Utils Added to utils/files
7. "app_label" removed from "TestConfig" & "ApiTest" Classes
8. Fixed Bug : 'LoggingModelManager' object has no attribute '_queryset_class'
9. Fixed : Logging Model not showing any records
10. Fixed : str method for base model, & removed current_timestamp method from base model
***

 ## Version 0.1.4
1. Fixed : ModuleNotFoundError: No module named 'pdf2docx'
2. Renamed “FileGenerator“ => “FileFactory”,
3. Add `create_` Prefix in FileFactory methods
4. Renamed MsbMetaModel -> MsbModelMetaFields
5. Added validation decorators, and fixed bulk validation issuses
6. Modified Logging Configuration Files
7. removed utils package
8. moved msb_core.wrappers.exceptions -> msb_exceptions
9. Fixed : Base ApiViews and Crud Routes
10. Searchparameter class refactored, search method added in ApiService Class
***

## Version 0.1.41
1. Fixed: Crud operations not working with encrypted id's
2. Package dependencies updated
3. Validator test cases refactored
***
## Version 0.1.5x
 ### -- Version 0.1.51
1. dbrouter print statement removed
2. datetime constants renamed (added _FORMAT to all fof them)
3. Fixed the default argument in msb_exception  which was causing "DESC :" to log even if desc was none
4. Api service create methdhod not working correctly
5. file logging handler is not registered in local env by default, we need to pass `emulate_prod=True` to add it 
6. SearchParameter class imported in package.__init__.py 
7. Fixed : test-cases are breaking because of logs databae
8. added base unittest class, and modified unit_test to inherit djangoTestCase instead of unittest
9. Added Validation Schema not defined exceptions
10. Fixed init_django_app error, int datatype instead of str while setting environement variable.
11. Added use_django decorator to use over classes/functions
12. Fixed : MsbMetaModel not working
13. MsbModel meta fields accessor added
14. Poetry dependencies updated
15. DMY_DATE_FORMAT added
16. versioning changed

  ### -- Version 0.1.52