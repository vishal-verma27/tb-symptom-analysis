import tb_model_predict, json
classifier = tb_model_predict.TuberculosisClassifierPredict("model\\tuberculosis_model.h5")
image_path = "dataset\\TB_Chest_Radiography_Database\\Normal\\Normal-1.png"
result = classifier.classify_image(image_path)
store_result = result.get('Actual')
# print("Output in JSON format:")
# result_01 = result.get('Label','Probability')
# print(json.dumps(result, indent=2))
# print(result_01)