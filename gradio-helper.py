import pickle 
import numpy as np
import pandas as pd

def fetch_pageviews(title):
    import pageviewapi
    retry_count = 0
    MAX_RETRIES = 10
    page_views = pageviewapi.per_article('en.wikipedia', title, '20150701', '20210607', access='all-access', agent='all-agents', granularity='daily')
    view_counter = 0
    for i in range (0, len(page_views['items'])):
        view_counter += page_views['items'][i]['views']
    
    return view_counter

def fetch_details_from_info_page(title):
    import requests
    url = "https://en.wikipedia.org/w/index.php?action=info&title=" + title

    html_content = requests.get(url)
    df_list = pd.read_html(html_content.text) # this parses all the tables in webpages to a list
    
    #Get Features from all tables

    #Basic info table
    try:
        display_title = df_list[1][1][0]
    except IndexError:
        print("IndexError for Basic info table, so skipping")
        return
    print("Display Title = ", display_title)

    # Process Table 1 - Basic Information
    dict_table1 = df_list[1].to_dict()
    
    #Declare vars
    page_length = ""
    page_id = ""
    number_page_watchers = ""
    number_page_watchers_recent_edits = ""
    page_views_past_30days = ""
    number_of_redirects = ""
    page_views_past_30days = ""
    total_edits = ""
    recent_number_of_edits = ""
    number_distinct_authors = ""
    number_categories = ""

    for key, value in dict_table1[0].items():  
        if value == 'Page length (in bytes)':        
            page_length = dict_table1[1][key]
            print("Page Length = ", page_length)
            
        elif (value == 'Page ID'):
            page_id = dict_table1[1][key]
            print("Scrapped Page ID = ", page_id)
            
        elif value == 'Number of page watchers':
            number_page_watchers = dict_table1[1][key]
            print("Number of Page Watchers = ", number_page_watchers)
        
        elif value == 'Number of page watchers who visited recent edits':
            number_page_watchers_recent_edits = dict_table1[1][key]
            print("Number of Page Watchers with recent edits = ", number_page_watchers_recent_edits)
        
        elif value == 'Number of redirects to this page':
            number_of_redirects = dict_table1[1][key]
            print("Number of redirects = ", number_of_redirects)
        
        elif value == 'Page views in the past 30 days':
            page_views_past_30days = dict_table1[1][key]
            print("Page views past 30 days = ", page_views_past_30days)
        
    #Process Table 3 - Edit History
    try:
        dict_table3 = df_list[3].to_dict()
        for key, value in dict_table3[0].items():  
            if value == 'Total number of edits':        
                total_edits = dict_table3[1][key]
                print("Total Edits = ", total_edits)
                
            elif value == 'Recent number of edits (within past 30 days)':
                recent_number_of_edits = dict_table3[1][key]
                print("Recent number of edits = ", recent_number_of_edits)
                
            elif value == 'Recent number of distinct authors':
                number_distinct_authors = dict_table3[1][key]
                print("Distinct authors =", number_distinct_authors)
    except IndexError:
        print("Couldn't find the Edit History Table, so skipping...")
        pass

    #Page properties Table
    try:
        categories_string = df_list[4][0][0]
        print(categories_string)
        number_categories = ""
        if  categories_string.startswith("Hidden categories"):         
            #Get number of categories
            for c in categories_string:
                if c.isdigit():
                    number_categories = number_categories + c     
            
            print("Total number of categories = ", number_categories)
    except IndexError:
        print("Couldn't find the Page Properties Table, so skipping...")
        pass

    print("============================================== EOP ======================================")

    features_dict = {   'page_length': page_length, 
                        'page_id': page_id, 
                        'number_page_watchers': number_page_watchers, 
                        'number_page_watchers_recent_edits': number_page_watchers_recent_edits, 
                        'number_of_redirects' : number_of_redirects, 
                        'page_views_past_30days' :page_views_past_30days, 
                        'total_edits': total_edits, 
                        'recent_number_of_edits': recent_number_of_edits, 
                        'number_distinct_authors': number_distinct_authors, 
                        'number_categories': number_categories }

    return features_dict

# MAP page_views and features_dict to np input array

def mapping_function(page_views, features_dict):

    features_of_test_sample = np.empty([12,])

    features_of_test_sample[0] = features_dict['page_id']
    features_of_test_sample[1] = page_views
    features_of_test_sample[2] = features_dict['page_length']
    features_of_test_sample[3] = features_dict['number_page_watchers']
    features_of_test_sample[4] = features_dict ['number_page_watchers_recent_edits']
    features_of_test_sample[5] = features_dict['number_of_redirects']
    features_of_test_sample[6] = features_dict['page_views_past_30days']
    features_of_test_sample[7] = features_dict['total_edits']
    features_of_test_sample[8] = features_dict['recent_number_of_edits']
    features_of_test_sample[9] = features_dict['number_distinct_authors']
    features_of_test_sample[10] = features_dict['number_categories']
    features_of_test_sample[11] = features_dict['page_id']
    
    wikipedia_url = "https://en.wikipedia.org/?curid=" + str(features_dict['page_id'])
    
    return features_of_test_sample, wikipedia_url

def get_features(title):
    #Get pageview
    page_views = fetch_pageviews(title)
    print('Tilte:', title, 'View Count:',page_views)
    
    #Get features from info pages 
    features_dict = fetch_details_from_info_page(title)
    
    #MAP both to numpy array
    features_of_test_sample, wikipedia_url = mapping_function(page_views, features_dict)
    
    return features_of_test_sample, wikipedia_url

def predict_protection_level(title):
    import pickle
    features_of_test_sample, wikipedia_url = get_features(title)
    print("Page URL: ", wikipedia_url)
    
    #Load the model
    filename = 'rfmodel.sav'
    loaded_model = pickle.load(open(filename, 'rb'))
    
    
    #predict    
    #print("Features 1st row:", X_test[0])
    y_pred = loaded_model.predict([features_of_test_sample])
    
    print("Predicted protection_level: ", y_pred[0])
    
    predicted_protection_level = y_pred    
    
    if(predicted_protection_level == 0):
        predicted_protection_level_str = "unprotected"
    elif(predicted_protection_level == 1):
        predicted_protection_level_str = "autoconfirmed"
    elif(predicted_protection_level == 2):
        predicted_protection_level_str = "extendedconfirmed"
    elif(predicted_protection_level == 3):
        predicted_protection_level_str = "sysop"
        
    return predicted_protection_level_str

def main():
    predicted_protection_level_str = predict_protection_level("Donald Trump")
    print("Protection level:", predicted_protection_level_str)

if __name__=='__main__':
    main()