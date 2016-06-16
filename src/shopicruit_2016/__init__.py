#!/usr/bin/python
try:
    # Python 3.0 and later
    from urllib.request import urlopen
except ImportError:
    # Back to Python 2's urllib2
    from urllib2 import urlopen

import json
import numpy as np

# To download data from store endpoint
def get_data_from_store():
    
    url_base = 'http://shopicruit.myshopify.com/products.json?page='
    page_id = 1
    products_page = ['start loading...']
    products_list = []
    
    while (len(products_page) > 0):
        
        # Retrieving data/page
        url = url_base + str(page_id)
        response = urlopen(url)
        products_data = json.loads(str(response.read()))
        
        # Assembling full product list
        products_page = products_data['products']
        products_list.extend(products_page)
        page_id += 1
        
    return products_list

# Extracting info related to computers/keyboards from full 
# product list
def filtering_desired_products(products_list):
    
    # Desired product types
    desired_types = ['keyboard','computer']
    # Reporting objects
    filtered_products = {desired_types[0]:[],desired_types[1]:[]}
    price_container = {desired_types[0]:[],desired_types[1]:[]}
    grams_container = {desired_types[0]:[],desired_types[1]:[]}
    
    # Looping over full product list
    for pindex in range(0,len(products_list)):
        p_object = products_list[pindex]
        p_type = p_object['product_type'].lower()
        # Looping over desired types
        for case in desired_types:
           if (p_type == case):
            p_variant = p_object['variants'] 
            # Unfolding product line into all available variants
            for vindex in range(0,len(p_variant)): 
               if p_variant[vindex]['available']:
                # Building mini-product object for later reporting
                  obj = {'name': p_object['title'],'variant':p_variant[vindex]['title'],
                  'price':p_variant[vindex]['price'],'grams':p_variant[vindex]['grams']}    
                  filtered_products[case].append(obj)
                  # Building price/grams lists 
                  price_container[case].append(obj['price'])
                  grams_container[case].append(obj['grams'])
               
    return filtered_products, price_container, grams_container

# Constructing and sorting price/grams matrices
def math_done_here(prices,grams):
   
    # Generating price and grams matrices for all combinations
    price_array_computer = np.asarray(prices['computer'],dtype='float')
    price_array_keyboard = np.asarray(prices['keyboard'],dtype='float')
    price_matrix = price_array_computer[:,None]+price_array_keyboard[None,:]
    
    grams_array_computer = np.asarray(grams['computer'],dtype='float')
    grams_array_keyboard = np.asarray(grams['keyboard'],dtype='float')
    grams_matrix = grams_array_computer[:,None]+grams_array_keyboard[None,:]
    
    # Sorting price matrix and getting reference row/colum indices for reporting
    indices_sorted = np.argsort(price_matrix.ravel())
    indices = np.arange(price_matrix.shape[0]*price_matrix.shape[1])
    row_ref = np.unravel_index(indices,price_matrix.shape)[0]
    col_ref = np.unravel_index(indices,price_matrix.shape)[1]
    
    return price_matrix, grams_matrix, indices_sorted, row_ref, col_ref

# Final report
def report_for_Alice(input_value):

    if input_value <= 0:
       print("Input for function has to be greater than zero")
    else:
      # Processing...
      products_list = get_data_from_store()
      filtered_products, prices, grams = \
      filtering_desired_products(products_list)
      price_matrix, grams_matrix, isorted, irow, icol = \
      math_done_here(prices,grams)
      max_items = len(isorted)

      # Integer input treat it as number of items to purchase
      if isinstance(input_value, int):
         max_index = input_value - 1
         if (max_index >= max_items - 1): max_index = max_items - 1      
         budget = 10e14 
      # Float input treat it as budget amount  
      if isinstance(input_value, float):
         budget = input_value
         max_index = max_items - 1

      # Initialization for reporting
      index = -1
      iref_next = isorted[index+1]
      total_paid = 0.0 
      total_grams = 0.0
   
      # Announce item variant list and results 
      print "Alice, here is all you can get for your request\n"
        
      while ((budget - total_paid > price_matrix[irow[iref_next]][icol[iref_next]]) and \
            (index < max_index)):
            index += 1
            iref = isorted[index]
            total_paid += price_matrix[irow[iref]][icol[iref]]  
            total_grams += grams_matrix[irow[iref]][icol[iref]]
            print "Choice", index+1, "costs: ", price_matrix[irow[iref]][icol[iref]], \
            "; weights in grams:", grams_matrix[irow[iref]][icol[iref]], \
            "; comprises: ", filtered_products['computer'][irow[iref]]['name'], "in", \
            filtered_products['computer'][irow[iref]]['variant'], "and", \
            filtered_products['keyboard'][icol[iref]]['name'], "in", \
            filtered_products['keyboard'][icol[iref]]['variant']        
 
            if index <= max_items - 2: 
               iref_next = isorted[index+1]
            else:
               print "\nYour input has maximized all possible combinations"  
      print "\nTotal cost (maximizes budget):", total_paid, \
            "\nTotal weight in grams:", total_grams, "\n"     

      return total_grams

