# pixsy-kafka
# Pixsy Fingerprinting and Classification

`git clone`

`pip install -r requirements.txt`

download deepranking model file from https://drive.google.com/file/d/1piEf1QU-jsrqOyhmiTpAgxmG9n2-7H5p/view?usp=sharing and save it in the `/models` folder.

To extract fingerprints of photos and matches in the `/images` folder, run:

`python feature_extractor.py -T photos`

`python feature_extractor.py -T matches`

The above two commands save the fingerprints in `/image_features` folder

To predict which of the matches are false positive, run:

`python predictor.py -P demo_photo_id.txt -M demo_match_ids.txt`

this saves the result in `demo_predictions.csv`

Edit the `demo_photo_id.txt` and `demo_match_ids.txt` files to compare different image pairs

Also, we can upload another set of images to the `/images` folder, and run `feature_extractor.py` and then `predictor.py`
