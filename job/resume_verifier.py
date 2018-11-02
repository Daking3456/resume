import os
# Configure settings for project
# Need to run this before calling models from application!
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'resume.settings')

import django
# Import settings
django.setup()
from django.conf import settings

from sklearn.externals import joblib
import dill


class Resume:
		
	def resume_verifier(text_file):
		print("I am here")
		print(text_file)
		open_pickle = open(os.path.join(settings.STATIC_ROOT, 'ML/doc_classifier_nb_model.sav'), 'rb')
		modl = joblib.load(open_pickle)
		open_pickle.close()

		raw_doc = []
		raw_doc.append(text_file)

		# Document Prediction [ 0 - Not Resume, 1 - Resume]
		doc_pred = modl.predict(raw_doc)
		print("____________________________________--______________________")
		print("Prediction:", doc_pred[0])
		print(doc_pred)
		print(type(doc_pred[0]))
		return True

	

# classify the domain in which given resume belongs to, e.g Python, Java, ..

	def resume_classifier(input_text):
		DICT_LABEL = {0: 'ANALYST', 1: 'SQL', 2: 'JAVA', 3: 'PYTHON', 4: '.NET', 5: 'AWS'}
		load_model = open(os.path.join(settings.STATIC_ROOT, 'ML/savedresumemodel.dill'), 'rb')
		mnb = dill.load(load_model)
		load_model.close()

		load_vect = open(os.path.join(settings.STATIC_ROOT, 'ML/savedvectorizer.dill'), 'rb')
		vect = dill.load(load_vect)
		load_vect.close()

		# Vectorize
		X_test_dtm = vect.transform([input_text])

		# Predict which given resume belongs to, e.g Python, Java, ..
		y_pred = mnb.predict(X_test_dtm)

		resume_class = DICT_LABEL[y_pred[0]]
		return resume_class

	def parse_resume():
		

		parsed_value = {'applied_for': 'Title',
						'personal_info':'Name Ram Shah \nAddress: Naxal\nContact 435234 \nEmail ram@shah.com',
						'education':'this is the education that is extrcted',
						'experience':'this is the values that we get for the experience',
						'skills':'this is the values that we get for the skills'
						}
		return parsed_value

	def filtered_jobs():
		job = (1,2,4)
		return job
