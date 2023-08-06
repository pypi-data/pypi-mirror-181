from QuantumPathQSOAPySDK import QSOAPlatform
qsoa = QSOAPlatform(configFile=True)



asset = qsoa.getAsset(22411, 'CIRCUIT', 'VL')

# print(type(asset.getDescription()))

new_assetName = 'newAssetName'
new_assetNamespace = 'newAssetNamespace'
new_assetDescription = 'newAssetDescription'
new_assetBody = 'circuit={"cols":[["H"]]}'

assetManagementData = qsoa.updateAsset(asset, new_assetName, new_assetNamespace, new_assetDescription, new_assetBody, 'GATES', 'VL')
# assetManagementData = qsoa.updateAsset(asset, new_assetName, new_assetNamespace, assetBody=new_assetBody, assetType='GATES', assetLevel='VL')