import sys
#
# @Orlando Guerra
#

def createObjectCache(cell,node,cacheName, jndiName, cache):
	objCache = AdminConfig.getid('/CacheInstance:'+cacheName+'/')
	if objCache:
		AdminConfig.remove(objCache) 
		print "Cache: ",cacheName
	newObjCache = AdminTask.createObjectCacheInstance('CacheProvider(cells/'+cell+'/nodes/'+node+'/servers/WebSphere_Portal/resources-pme502.xml#CacheProvider_1055745612404)', '[-name ' + cacheName + ' -jndiName ' + jndiName + ']')
	AdminConfig.modify(newObjCache, '[[cacheSize ' + cache + ']]')
	print " Object Cache: ",cacheName, " created with > JNDI: ", jndiName
	
	
def createEnvJVM(service, name, value):	
	newrep = AdminConfig.getid('/ResourceEnvironmentProvider:'+service+'/')
	propSet = AdminConfig.showAttribute(newrep, 'propertySet')
	resourceProperties = AdminConfig.list("J2EEResourceProperty", propSet).splitlines()
	for resourceProperty  in resourceProperties:
		if (AdminConfig.showAttribute(resourceProperty, "name") == name):
			AdminConfig.remove(resourceProperty)
			print name + ' Deleted' 
			break	
	newrep = AdminConfig.getid('/ResourceEnvironmentProvider:'+service+'/')
	propSet = AdminConfig.showAttribute(newrep, 'propertySet')
	print AdminConfig.create('J2EEResourceProperty', propSet, [["name",name], ["value",value]])
	
	
def createPropertyJVM(propName,value,node,serverName):
	prop = AdminConfig.getid('/Node:'+node+'/Server:'+serverName+'/JavaProcessDef:/JavaVirtualMachine:/Property:'+propName+'/')
	if prop:
		AdminConfig.remove(prop) 
		print 'property removed:'+prop	
	jvm = AdminConfig.list("JavaVirtualMachine", servern)
	print jvm
	AdminConfig.create('Property', jvm, [ ['name', propName], ['value', value] ], 'systemProperties')
	
	
def createSpaceBinding(nameInNameSpaceVal,value, node, servern, serverName):
	wcm = AdminConfig.getid('/Node:'+node+'/Server:'+serverName+'/StringNameSpaceBinding:'+nameInNameSpaceVal+'/')
	if wcm:
		AdminConfig.remove(wcm) 
		print "Name Space: ",nameInNameSpaceVal, " Exists ", value
	AdminConfig.create('StringNameSpaceBinding',servern,'[[name '+nameInNameSpaceVal+'] [nameInNameSpace '+nameInNameSpaceVal+'] [stringToBind '+value+']]')
	
	
cell = AdminControl.getCell()
node = AdminControl.getNode()	
server = AdminControl.getConfigId(AdminControl.queryNames("node="+node+",type=Server,*"))
servern = AdminConfig.getid('/Node:'+node+'/Server:WebSphere_Portal/')
serverName = AdminConfig.showAttribute(servern, 'name') 

createObjectCache(cell,node,'RegistrationCenterCache','services/cache/RegistrationCenterCache','50000')
createObjectCache(cell,node,'RegistrationAppletCache','services/cache/RegistrationAppletCache','50000')
createObjectCache(cell,node,'RegistrationAttributeCache','services/cache/RegistrationAttributeCache','50000')
createObjectCache(cell,node,'RegistrationMessageCache','services/cache/RegistrationMessageCache','50000')
createObjectCache(cell,node,'RegistrationQueueCache','services/cache/RegistrationQueueCache','50000');
createObjectCache(cell,node,'RegistrationWizardCache','services/cache/RegistrationWizardCache','50000');
createObjectCache(cell,node,'FwSessionCache','services/cache/FwSessionCache','10000');
createObjectCache(cell,node,'FwContentCache','services/cache/FwContentCache','200000');
createObjectCache(cell,node,'ApplicationRefTableCache','services/cache/ApplicationRefTableCache','100000');

createObjectCache(cell,node,'AppletContentCache','services/cache/AppletContentCache','200000');
createObjectCache(cell,node,'AttributeContentCache','services/cache/AttributeContentCache','200000');
createObjectCache(cell,node,'CenterContentCache','services/cache/CenterContentCache','200000');
createObjectCache(cell,node,'MessageContentCache','services/cache/MessageContentCache','200000');
createObjectCache(cell,node,'WizardContentCache','services/cache/WizardContentCache','200000');


createEnvJVM('WP NavigatorService','public.session','true')	
createEnvJVM('WP StateManagerService','com.ibm.wps.state.preprocessors.locale.CookieSupportedLanguagePreProcessor.cookie.maxage','-1')	
createEnvJVM('WP StateManagerService','preprocessors','com.ibm.wps.state.preprocessors.urlmapping.URLMappingPreProcessor,com.ibm.wps.resolver.friendly.preprocessors.FriendlyPreProcessor,com.ibm.wps.resolver.portal.ResolvedPreprocessor,com.ibm.wps.state.preprocessors.selection.StandardPortalSelectionImpl,com.ibm.wps.state.preprocessors.selection.FragmentSelectionImpl,com.ibm.wps.state.preprocessors.selection.ResourceSelectionImpl,com.ibm.wps.state.preprocessors.eclipse.ExtensionPreProcessor,com.ibm.wps.state.preprocessors.portlet.RequestParameterMerger,com.ibm.wps.state.preprocessors.locale.CookieSupportedLanguagePreProcessor')	

createPropertyJVM('com.ibm.ws.cache.CacheConfig.showObjectContents','true', node, serverName)

createSpaceBinding('FW_AUTH_WCM_HOST','http://cwad501.hhscie.txaccess.net',node, servern ,serverName)
createSpaceBinding('FW_AUTH_WCM_PORT','12039',node, servern ,serverName)

createSpaceBinding('FW_WCM_HOST','http://wcm-pfx-vip.hhscie.txaccess.net',node, servern ,serverName)
createSpaceBinding('FW_WCM_PORT','80',node, servern ,serverName)
createSpaceBinding('FW_WCM_CONTEXT_ROOT','HHSC_wcmcache',node, servern ,serverName)

createSpaceBinding('FW_REMOTE_SERVERS','ea990-82014372.hhsea.txnet.state.tx.us:10039,ea990-82014345.hhsea.txnet.state.tx.us:10039,hhsld0082014497.hhsea.txnet.state.tx.us:10039',node, servern ,serverName)
createSpaceBinding('FW_CODE_VERSION','4.5.0.6',node, servern ,serverName)

createSpaceBinding('AGING_ENABLED_FLAG','TRUE',node, servern ,serverName)

AdminConfig.save()
print "YTB Portal Configured and saved"

