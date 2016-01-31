1. Data source for MatchMaker dataset: agesonly.csv, matchmaker.csv
  * The agesonly.csv only includes matched ages since it is easier to visualize 2 variables.
  * The matchmaker.csv contains each individual info as each row, the last element in each row (0 or 1) indicates whether this person is a good match..... (I think, if someone is not a good match, why use dating website... There is no real bad match, it's just because they didn't find the right match... but here, it may make the prediction easier).
  
2. load_match_data.py
  * Load .cvs match data and generate a list of matchrow objects. Each object contains data as the person's info, and is_good_match to to indicate whether the person is a good match.
