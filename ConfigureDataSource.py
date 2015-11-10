import sys
#
# @Orlando Guerra
#

user = "user";
pwd = "pwd";
urlDS = "(DESCRIPTION=(ENABLE=BROKEN)... this will be modified1";
#Include all the dynamic examples


node = AdminTask.listNodes();


dsSSP = AdminConfig.getid('/DataSource:SSP/')
if dsSSP:
	AdminConfig.remove(dsSSP)
	AdminTask.deleteAuthDataEntry('[-alias YTB/ssp_local ]')

	
ds = AdminConfig.getid('/JDBCProvider:Oracle JDBC Driver/')	
if ds:
	AdminConfig.remove(ds)

jdbcprov =  AdminTask.createJDBCProvider('[-scope Node='+node+',Server=server1 -databaseType Oracle -providerType "Oracle JDBC Driver" -implementationType "Connection pool data source" -name "Oracle JDBC Driver" -description "Oracle JDBC Driver" -classpath [C:/oracle/product/11.2.0/client_1/jdbc/lib/ojdbc6.jar ] -nativePath "" ]')

print AdminTask.createAuthDataEntry('[-alias ssp_local -user '+user+' -password '+pwd+' -description '+user+' ]')
print AdminTask.createDatasource(jdbcprov, '[-name SSP -jndiName jdbc/sspdatasource -dataStoreHelperClassName com.ibm.websphere.rsadapter.Oracle11gDataStoreHelper -containerManagedPersistence true -componentManagedAuthenticationAlias '+node+'/ssp_local -configureResourceProperties [[URL java.lang.String jdbc:oracle:thin:@'+urlDS+']]]')
	

AdminConfig.save()

print "Datasources Configured and saved"



