# ge-kada-plugin

### Steps to use the KadaStoreValidationResultsAction from the plugin

1. Install the plugin by `pip install kada-ge-store-plugin`. You can put `kada-ge-store-plugin` in the requirements.txt file for CI/CD operations. You'll also need the following two Azure modules:

    * azure.identity
    * azure.storage.blob

These will be installed as dependencies so you won't have to install them.

2. In your required `checkpoint`, add the following action to your checkpoint `.yml` file.

```yml
  - name: store_kada_validation_result
    action:
      class_name: KadaStoreValidationResultsAction
      module_name: kada_ge_store_plugin.kada_store_validation
      container: ${VALIDATIONS_CONTAINER}
      prefix: lz/ge_landing/landing
      connection_string: DefaultEndpointsProtocol=https;AccountName=${STORAGE_ACCOUNT_NAME};AccountKey=${STORAGE_ACCOUNT_KEY};EndpointSuffix=core.windows.net
      account_url: ${SAS_URL}
      access_key: ${SAS_TOKEN}
```

You should change the prefix to your desired nested blob storage. Preference will be given to the `connection_string` as a connection method to the Azure storage account. If you are using storage access url and token, remove the `connection_string`. 

3. In your uncommited/config_variables.yml file or if you are using environment variables, add the following variables related to the azure storage account:

    * VALIDATIONS_CONTAINER

    Either:

    * STORAGE_ACCOUNT_NAME
    * STORAGE_ACCOUNT_KEY

    Or:

    * SAS_URL
    * SAS_TOKEN
    
4. Add/Change the `run_name_template` in your checkpoint `.yml` file to `'%Y%m%d%H%M%S'`.

### Note

If your checkpoint's `action_list` contains a `StoreValidationResultAction`, the validation results will get stored in the given validtions store inside `great_expectations.yml` file and also in the Azure Storage container with the custom `.json` filename. Basically, you'll be storing validation results in 2 different places.

Since this is a new plugin, it might be worthwhile keeping the `StoreValidationResultAction` to make sure the validation results are getting stored even with a failure in this plugin.

### Note

Added tags to facilitate version releasing and CI/CD operations
