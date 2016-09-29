from mfcmontage import helper, montage, wished

username = 'MilkyTaste'

statusCode = helper.getStatusCode('owned')
montage.montageStatus(username, statusCode)
wished.montageWished(username)
