with open("artifacts/ModelTrainerArtifacts/last_run_id.txt", "r") as f:
    run_id = f.read()


print(run_id)


logging.info("fetching best model from gcloud syncer")
                #best_model_path = self.get_best_model_from_gcloud()
                best_model_path = ""

                logging.info("Check is best model present in the gcloud storage or not")
                if os.path.isfile(best_model_path) is False:
                    is_model_accepted = True
                    logging.info("gcloud storage model is false and currently trained model accpeted is true")

                else:
                    logging.info("Load best model fetched from gcloud storage")
                    best_model = keras.models.load_model(best_model_path)
                    best_model_accuracy = self.evaluate(tokenizer, best_model)

                    logging.info("comparing loss between best_model_loss and trained_model_loss ?")

                    if best_model_accuracy > trained_model_accuracy:
                        is_model_accepted = True
                        logging.info("Trained model not accepted")
                    else:
                        is_model_accepted = False
                        logging.info("Trained model accepted")