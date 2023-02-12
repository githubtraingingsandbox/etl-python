import pandas as pd
import random
import uuid
import string
import json
from faker import Faker
from datetime import datetime, timedelta
import configparser
import os 
import time
import logging, coloredlogs
from pathlib import Path


def generate_travel_data():


  # ================================================ LOGGER ================================================

  # Set up root root_logger 
  root_logger     =   logging.getLogger(__name__)
  root_logger.setLevel(logging.DEBUG)


  # Set up formatter for logs 
  file_handler_log_formatter      =   logging.Formatter('%(asctime)s  |  %(levelname)s  |  %(message)s  ')
  console_handler_log_formatter   =   coloredlogs.ColoredFormatter(fmt    =   '%(message)s', level_styles=dict(
                                                                                                  debug           =   dict    (color  =   'white'),
                                                                                                  info            =   dict    (color  =   'green'),
                                                                                                  warning         =   dict    (color  =   'orange'),
                                                                                                  error           =   dict    (color  =   'red',      bold    =   True,   bright      =   True),
                                                                                                  critical        =   dict    (color  =   'black',    bold    =   True,   background  =   'red')
                                                                                              ),

                                                                                      field_styles=dict(
                                                                                          messages            =   dict    (color  =   'white')
                                                                                      )
                                                                                      )


  # Set up file handler object for logging events to file
  current_filepath    =   Path(__file__).stem
  file_handler        =   logging.FileHandler('logs/L0_src_data_generator/' + current_filepath + '.log', mode='w')
  file_handler.setFormatter(file_handler_log_formatter)


  # Set up console handler object for writing event logs to console in real time (i.e. streams events to stderr)
  console_handler     =   logging.StreamHandler()
  console_handler.setFormatter(console_handler_log_formatter)


  # Add the file and console handlers 
  root_logger.addHandler(file_handler)
  

    # Only add the console handler if the script is running directly from this location 
  if __name__=="__main__":
      root_logger.addHandler(console_handler)


  # Establish the relevant constants for generating the synthetic travel data 

  NO_OF_CUSTOMER_INFO_ROWS = 100
  NO_OF_FLIGHT_SCHEDULES = 100
  NO_OF_CUSTOMER_FEEDBACKS = 100
  NO_OF_TICKET_PRICES = 100
  NO_OF_FLIGHT_BOOKINGS = 100
  NO_OF_FLIGHT_DESTINATIONS = 100
  NO_OF_FLIGHT_TICKET_SALES = 100
  NO_OF_FLIGHT_PROMOS_AND_DEALS = 100
  NO_OF_SALES_AGENTS = 100
  NO_OF_ACCOMMODATION_BOOKINGS = 400 


  # Set up environment variables 
  config = configparser.ConfigParser()
  path = os.path.abspath('dwh_pipelines/local_config.ini')
  config.read(path)

  DATASETS_LOCATION_PATH = config['travel_data_filepath']['DATASETS_LOCATION_PATH']




  root_logger.debug("")
  root_logger.debug("")
  root_logger.debug("Now beginning session for generating data...")

  # ========================================================================================================================================================================

  # ============================ CUSTOMER INFORMATION ============================

   # Create a Faker instance to generate fake data
  CUSTOMER_INFO_PROCESSING_START_TIME = time.time()
  fake = Faker()


  created_date = fake.date_this_decade()
  
  preferred_contact_method = [
  {"id": uuid.uuid4(), "description": "Email"},
  {"id": uuid.uuid4(), "description": "Phone"},
  {"id": uuid.uuid4(), "description": "Text message"},
  {"id": uuid.uuid4(), "description": "Postal mail"},
  {"id": uuid.uuid4(), "description": "No contact"}
]



  customer_info_records = []

  for i in range(NO_OF_CUSTOMER_INFO_ROWS):

    customer_info_record = {
      'customer_id': uuid.uuid4(),
      'first_name': fake.first_name(),
      'last_name': fake.last_name(),
      'email': f"{fake.first_name().lower()}.{fake.last_name().lower()}@" + random.choice(['email.com', 'inlook.com', 'mzn.com', 'aio.net', 'macrosoft.com' ]),
      'place_of_birth': fake.city(),
      'dob' : fake.date_of_birth(),
      'age': random.uniform(1, 100),
      'address': fake.address(),
      'city': fake.city(),
      'state': fake.state(),
      'zip': fake.zipcode(),
      'phone_number': fake.phone_number(),
      'credit_card': fake.credit_card_number(),
      'credit_card_provider': fake.credit_card_provider(),
      'nationality': fake.country(),
      'created_date': created_date,
      'last_updated_date': created_date + pd.Timedelta(days=random.randint(1, 40)),
      'customer_contact_preference_id': str(uuid.uuid4()),
      'customer_contact_preference_desc': random.choice(list(preferred_contact_method))
    }
    customer_info_records.append(customer_info_record)


  customer_info_df = pd.DataFrame(customer_info_records)
  # root_logger.info(customer_info_df)


   # Write dataframe to JSON file
  with open(f'{DATASETS_LOCATION_PATH}/customer_info.json', 'w') as customer_info_file:
      customer_info_df_to_json = customer_info_df.to_json(orient="records", default_handler=str)
      customer_info_df_to_json = json.loads(customer_info_df_to_json)
      customer_info_file.write(json.dumps(customer_info_df_to_json, indent=4, sort_keys=True)) 

    

 


  # Print the customer information title in console
  root_logger.info('----------')
  root_logger.info('============================ CUSTOMER INFORMATION ============================')
  root_logger.info(customer_info_df)
  

  CUSTOMER_INFO_PROCESSING_END_TIME = time.time()

  # ========================================================================================================================================================================



  # ============================ FLIGHT SCHEDULES ============================

   # Create a Faker instance to generate fake data
  FLIGHT_SCHEDULES_PROCESSING_START_TIME = time.time()
  fake = Faker()


  flight_schedules = []
  for i in range(NO_OF_FLIGHT_SCHEDULES):
    flight_schedule = {
    'flight_id' : uuid.uuid4(),
    'departure_city' : fake.city(),
    'arrival_city' : fake.city(),
    'departure_time' : fake.time(),
    'arrival_time' : fake.time(),
    'flight_date' : fake.date_this_decade()

    }
    flight_schedules.append(flight_schedule)


    flight_schedules_df = pd.DataFrame(flight_schedules)
    # root_logger.info(flight_schedules_df)


     # Write dataframe to JSON file
  with open(f'{DATASETS_LOCATION_PATH}/flight_schedules.json', 'w') as flight_schedules_file:
      flight_schedules_df_to_json = flight_schedules_df.to_json(orient="records", default_handler=str)
      flight_schedules_df_to_json = json.loads(flight_schedules_df_to_json)
      flight_schedules_file.write(json.dumps(flight_schedules_df_to_json, indent=4, sort_keys=True)) 

    

 


  # Print the customer information title in console
  root_logger.info('----------')
  root_logger.info('============================ FLIGHT SCHEDULES ============================')
  root_logger.info(flight_schedules_df)
  FLIGHT_SCHEDULES_PROCESSING_END_TIME = time.time()
  


  # ========================================================================================================================================================================


   # ============================ TICKET PRICES ============================

   # Create a Faker instance to generate fake data
  TICKET_PRICES_PROCESSING_START_TIME = time.time()
  fake = Faker()


  ticket_prices = []
  for i in range(NO_OF_TICKET_PRICES):
     ticket_price = {
        'flight_id' : random.choice(flight_schedules_df['flight_id']),
        'ticket_price': random.randint(50, 700),
        'ticket_price_date': fake.date_this_decade()

     }
     ticket_prices.append(ticket_price)

  ticket_prices_df = pd.DataFrame(ticket_prices)

  # Write dataframe to JSON file
  with open(f'{DATASETS_LOCATION_PATH}/ticket_prices.json', 'w') as ticket_prices_file:
      ticket_prices_df_to_json = ticket_prices_df.to_json(orient="records", default_handler=str)
      ticket_prices_df_to_json = json.loads(ticket_prices_df_to_json)
      ticket_prices_file.write(json.dumps(ticket_prices_df_to_json, indent=4, sort_keys=True)) 



  # Print the customer information title in console
  root_logger.info('----------')
  root_logger.info('============================ TICKET PRICES ============================')
  root_logger.info(ticket_prices_df)
  TICKET_PRICES_PROCESSING_END_TIME = time.time()
  



  # ============================ FLIGHT BOOKINGS ============================

   # Create a Faker instance to generate fake data
  FLIGHT_BOOKINGS_PROCESSING_START_TIME = time.time()
  fake = Faker()


  flight_bookings = []

  for i in range(NO_OF_FLIGHT_BOOKINGS):
     flight_booking = {
        'flight_booking_id': uuid.uuid4(),
        'customer_id' : random.choice(customer_info_df['customer_id']),
        'flight_id' : random.choice(flight_schedules_df['flight_id']),
        'ticket_price' : random.randint(0, 700),
        'booking_date': fake.date_this_decade(),
        'payment_method': random.choice(['Credit card', 'Debit card', 'PayPal', 'Bank transfer']),
        'confirmation_code': ''.join(random.choices(string.ascii_uppercase + string.digits, k=10)),
        'checked_in': random.choice(['Yes', 'No'])
     }
     flight_bookings.append(flight_booking)
  

  flight_bookings_df = pd.DataFrame(flight_bookings)

  # Write dataframe to JSON file
  with open(f'{DATASETS_LOCATION_PATH}/flight_bookings.json', 'w') as flight_bookings_file:
      flight_bookings_df_to_json = flight_bookings_df.to_json(orient="records", default_handler=str)
      flight_bookings_df_to_json = json.loads(flight_bookings_df_to_json)
      flight_bookings_file.write(json.dumps(flight_bookings_df_to_json, indent=4, sort_keys=True)) 



  # Print the customer information title in console
  root_logger.info('----------')
  root_logger.info('============================ FLIGHT BOOKINGS ============================')
  root_logger.info(flight_bookings_df)
  FLIGHT_BOOKINGS_PROCESSING_END_TIME = time.time()
  




  # ============================ CUSTOMER FEEDBACK ============================

   # Create a Faker instance to generate fake data
  CUSTOMER_FEEDBACKS_PROCESSING_START_TIME = time.time()
  fake = Faker()


  customer_feedbacks = []
  for i in range(NO_OF_CUSTOMER_FEEDBACKS):
     customer_feedback = {
     'feedback_id' : uuid.uuid4(),
     'customer_id': random.choice(customer_info_df['customer_id']),
     'flight_booking_id': random.choice(flight_bookings_df['flight_booking_id']),
     'feedback_text': fake.text(),
     'feedback_date': fake.date_this_decade()
     }

     customer_feedbacks.append(customer_feedback)


  
  customer_feedbacks_df = pd.DataFrame(customer_feedbacks)

  # Write dataframe to JSON file
  with open(f'{DATASETS_LOCATION_PATH}/customer_feedbacks.json', 'w') as customer_feedbacks_file:
      customer_feedbacks_df_to_json = customer_feedbacks_df.to_json(orient="records", default_handler=str)
      customer_feedbacks_df_to_json = json.loads(customer_feedbacks_df_to_json)
      customer_feedbacks_file.write(json.dumps(customer_feedbacks_df_to_json, indent=4, sort_keys=True)) 



  # Print the customer information title in console
  root_logger.info('----------')
  root_logger.info('============================ CUSTOMER FEEDBACKS ============================')
  root_logger.info(customer_feedbacks_df)
  CUSTOMER_FEEDBACKS_PROCESSING_END_TIME = time.time()
  
    

  # ============================ SALES AGENTS ============================


  SALES_AGENTS_PROCESSING_START_TIME = time.time()
  fake = Faker()

  

  # List of sales agents
  agents = []

  # Generate the sales agents
  for i in range(NO_OF_SALES_AGENTS):
    agent_id = str(uuid.uuid4())
    first_name = fake.first_name()
    last_name = fake.last_name()
    email = f"{first_name.lower()}.{last_name.lower()}@" + random.choice(['gmail.com', 'outlook.com', 'msn.com', 'aoi.net', 'microsoft.com' ])
    phone = fake.phone_number()
    location = fake.city()
    service_speciality = random.choice(['Air', 'Land', 'Sea'])
    years_experience = random.randint(1, 10)
    commission = random.uniform(0.1, 0.3)
    nationality = fake.country()
    seniority_levels = ['Junior', 'Mid-Level', 'Senior']
    seniority_level = random.choice(seniority_levels)
    agents.append({
        'id': agent_id,
        'first_name': first_name,
        'last_name': last_name,
        'email': email,
        'phone': phone,
        'location': location,
        'service_speciality': service_speciality,
        'years_experience': years_experience,
        'commission': commission,
        'nationality': nationality,
        'seniority_level': seniority_level
    })

  # Create a Pandas DataFrame from the list of options
  sales_agents_df = pd.DataFrame(agents)


  # # Write dataframe to JSON file 
  with open(f'{DATASETS_LOCATION_PATH}/sales_agents.json', 'w') as sales_agents_file:
    sales_agents_file_df_to_json = sales_agents_df.to_json(orient="records")
    sales_agents_file.write(json.dumps(json.loads(sales_agents_file_df_to_json), indent=4, sort_keys=True)) 


  # Print the data frame
  root_logger.info('----------')
  root_logger.info('============================ SALES AGENTS ============================')
  root_logger.info(sales_agents_df)
  SALES_AGENTS_PROCESSING_END_TIME = time.time()





  # ============================ FLIGHT DESTINATION ============================

   # Create a Faker instance to generate fake data
  FLIGHT_DESTINATION_PROCESSING_START_TIME = time.time()
  fake = Faker()

  flight_destinations = []

  for i in range(NO_OF_FLIGHT_DESTINATIONS):
     flight_destination = {
        'flight_id' : random.choice(flight_bookings_df['flight_id']),
        'departure_city' : fake.city(),
        'arrival_city': fake.city() 

     }

     flight_destinations.append(flight_destination)

  flight_destinations_df = pd.DataFrame(flight_destinations)

  # Write dataframe to JSON file
  with open(f'{DATASETS_LOCATION_PATH}/flight_destinations.json', 'w') as flight_destinations_file:
      flight_destinations_df_to_json = flight_destinations_df.to_json(orient="records", default_handler=str)
      flight_destinations_df_to_json = json.loads(flight_destinations_df_to_json)
      flight_destinations_file.write(json.dumps(flight_destinations_df_to_json, indent=4, sort_keys=True)) 



  # Print the customer information title in console
  root_logger.info('----------')
  root_logger.info('============================ FLIGHT DESTINATIONS ============================')
  root_logger.info(flight_destinations_df)
  FLIGHT_DESTINATION_PROCESSING_END_TIME = time.time()
  
    


  # ============================ FLIGHT PROMOTIONS & DEALS ============================

   # Create a Faker instance to generate fake data
  FLIGHT_PROMOTIONS_PROCESSING_START_TIME = time.time()
  fake = Faker()

  flight_promotion_deals = []

  for i in range(NO_OF_FLIGHT_PROMOS_AND_DEALS):
     flight_promotion_deal = {
        'promotion_id': uuid.uuid4(),
        'promotion_name': fake.sentence(), 
        'flight_booking_id': random.choice(flight_bookings_df['flight_booking_id']),
        'applied_discount': random.randint(10, 350)

     }
     flight_promotion_deals.append(flight_promotion_deal)

  
  flight_promotion_deals_df = pd.DataFrame(flight_promotion_deals)

    # Write dataframe to JSON file
  with open(f'{DATASETS_LOCATION_PATH}/flight_promotion_deals.json', 'w') as flight_promotion_deals_file:
      flight_promotion_deals_df_to_json = flight_promotion_deals_df.to_json(orient="records", default_handler=str)
      flight_promotion_deals_df_to_json = json.loads(flight_promotion_deals_df_to_json)
      flight_promotion_deals_file.write(json.dumps(flight_promotion_deals_df_to_json, indent=4, sort_keys=True)) 



  # Print the customer information title in console
  root_logger.info('----------')
  root_logger.info('============================ FLIGHT PROMOTIONS & DEALS ============================')
  root_logger.info(flight_promotion_deals_df)
  FLIGHT_PROMOTIONS_PROCESSING_END_TIME = time.time()
  

     


  # ============================ FLIGHT TICKET SALES ============================

   # Create a Faker instance to generate fake data
  FLIGHT_TICKET_SALES_PROCESSING_START_TIME = time.time()
  fake = Faker()

  flight_ticket_sales = []

  for i in range(NO_OF_FLIGHT_TICKET_SALES):
     flight_ticket_sale = {
        'flight_booking_id': random.choice(flight_bookings_df['flight_id']),
        'customer_id': random.choice(customer_info_df['customer_id']),
        'customer_first_name': random.choice(customer_info_df['first_name']),
        'customer_last_name': random.choice(customer_info_df['last_name']),
        'agent_id': random.choice(sales_agents_df['id']),
        'agent_first_name': random.choice(sales_agents_df['first_name']),
        'agent_last_name': random.choice(sales_agents_df['last_name']),
        'ticket_sales': random.randint(100, 500),
        'ticket_sales_date': fake.date_this_decade(),
        'promotion_id': random.choice(flight_promotion_deals_df['promotion_id']),
        'promotion_name': random.choice(flight_promotion_deals_df['promotion_name']),
        'discount': random.choice(flight_promotion_deals_df['applied_discount']),
     }

     flight_ticket_sales.append(flight_ticket_sale)
  
  flight_ticket_sales_df = pd.DataFrame(flight_ticket_sales)

  # Write dataframe to JSON file
  with open(f'{DATASETS_LOCATION_PATH}/flight_ticket_sales.json', 'w') as flight_ticket_sales_file:
      flight_ticket_sales_df_to_json = flight_ticket_sales_df.to_json(orient="records", default_handler=str)
      flight_ticket_sales_df_to_json = json.loads(flight_ticket_sales_df_to_json)
      flight_ticket_sales_file.write(json.dumps(flight_ticket_sales_df_to_json, indent=4, sort_keys=True)) 



  # Print the customer information title in console
  root_logger.info('----------')
  root_logger.info('============================ FLIGHT TICKET SALES ============================')
  root_logger.info(flight_ticket_sales_df)
  FLIGHT_TICKET_SALES_PROCESSING_END_TIME = time.time()
  

     



  # ============================ ACCOMMODATION BOOKINGS ============================

   # Create a Faker instance to generate fake data
  ACCOMMODATION_BOOKINGS_PROCESSING_START_TIME = time.time()
  fake = Faker()

  accommodation_options = ['Drayton Manners Hotel', 'Hannah Wilson Hotel', 'Ladberry Sapphire Hotel', 'D.Q Hotel', 'Royal Baked Beans Hotel', 'Breakfast Abroad Hotel', 'Benny Toast Hotel', 'Test DWH Hotel']
  check_in_date = random.choice(pd.date_range(start='2012-01-01', end='2022-12-31'))

  accommodation_bookings = []

  for i in range(NO_OF_ACCOMMODATION_BOOKINGS):
     accommodation_booking = {
        'id': uuid.uuid4(),
        'location' : fake.city(),
        'room_type' : random.choice(["Single", "Double", "Family", "Luxury"]),
        'check_in_date' : check_in_date,
        'check_out_date' : check_in_date + pd.Timedelta(days=random.randint(1, 14)),
        'booking_date' : random.choice(pd.date_range(start='2012-01-01', end='2022-12-31')),
        'total_price' : random.randint(50, 500),
        'customer_id' : random.choice(customer_info_df['customer_id']),
        'flight_booking_id' : random.choice(flight_bookings_df['flight_booking_id']),
        'sales_agent_id': random.choice(sales_agents_df['id']),
        'num_adults': random.randint(1, 4),
        'num_children': random.randint(0, 2),
        'total_price': random.uniform(100, 1000),
        'status': random.choice(['Confirmed', 'Cancelled', 'Pending']),
        'payment_method': random.choice(['Credit card', 'Debit card', 'PayPal', 'Bank transfer']),
        'confirmation_code': ''.join(random.choices(string.ascii_uppercase + string.digits, k=10)),
        'checked_in': random.choice(['Yes', 'No'])
     
     }
     accommodation_bookings.append(accommodation_booking)
  

  accommodation_bookings_df = pd.DataFrame(accommodation_bookings)

  # Write dataframe to JSON file
  with open(f'{DATASETS_LOCATION_PATH}/accommodation_bookings.json', 'w') as accommodation_bookings_file:
      accommodation_bookings_df_to_json = accommodation_bookings_df.to_json(orient="records", default_handler=str)
      accommodation_bookings_df_to_json = json.loads(accommodation_bookings_df_to_json)
      accommodation_bookings_file.write(json.dumps(accommodation_bookings_df_to_json, indent=4, sort_keys=True)) 



  # Print the customer information title in console
  root_logger.info('----------')
  root_logger.info('============================ ACCOMMODATION BOOKINGS ============================')
  root_logger.info(accommodation_bookings_df)
  ACCOMMODATION_BOOKINGS_PROCESSING_END_TIME = time.time()
  
     




 
  root_logger.info(f'')
  root_logger.info(f'')
  root_logger.info('================================================')
  root_logger.info('              DATA PROFILING METRICS              ')
  root_logger.info('================================================')
  root_logger.info(f'')
  root_logger.info(f'Now calculating statistics for data generated ...')
  root_logger.info(f'')
  root_logger.info(f'')
  root_logger.info(f'')
  root_logger.info(f'')


  # Define constants for query execution times 
  EXECUTION_TIME_FOR_GENERATING_CUSTOMER_INFO                      =     (  CUSTOMER_INFO_PROCESSING_END_TIME             -      CUSTOMER_INFO_PROCESSING_START_TIME            )   *   1000
  EXECUTION_TIME_FOR_GENERATING_FLIGHT_SCHEDULES                   =     (  FLIGHT_SCHEDULES_PROCESSING_END_TIME          -      FLIGHT_SCHEDULES_PROCESSING_START_TIME         )   *   1000
  EXECUTION_TIME_FOR_GENERATING_TICKET_PRICES                      =     (  TICKET_PRICES_PROCESSING_END_TIME             -      TICKET_PRICES_PROCESSING_START_TIME            )   *   1000
  EXECUTION_TIME_FOR_GENERATING_FLIGHT_BOOKINGS                    =     (  FLIGHT_BOOKINGS_PROCESSING_END_TIME           -      FLIGHT_BOOKINGS_PROCESSING_START_TIME          )   *   1000
  EXECUTION_TIME_FOR_GENERATING_CUSTOMER_FEEDBACKS                 =     (  CUSTOMER_FEEDBACKS_PROCESSING_END_TIME        -      CUSTOMER_FEEDBACKS_PROCESSING_START_TIME       )   *   1000
  EXECUTION_TIME_FOR_GENERATING_SALES_AGENTS                       =     (  SALES_AGENTS_PROCESSING_END_TIME              -      SALES_AGENTS_PROCESSING_START_TIME             )   *   1000
  EXECUTION_TIME_FOR_GENERATING_FLIGHT_DESTINATIONS                =     (  FLIGHT_DESTINATION_PROCESSING_END_TIME        -      FLIGHT_DESTINATION_PROCESSING_START_TIME       )   *   1000
  EXECUTION_TIME_FOR_GENERATING_FLIGHT_PROMOS_AND_DEALS            =     (  FLIGHT_PROMOTIONS_PROCESSING_END_TIME         -      FLIGHT_PROMOTIONS_PROCESSING_START_TIME        )   *   1000
  EXECUTION_TIME_FOR_GENERATING_FLIGHT_TICKET_SALES                =     (  FLIGHT_TICKET_SALES_PROCESSING_END_TIME       -      FLIGHT_TICKET_SALES_PROCESSING_START_TIME      )   *   1000
  EXECUTION_TIME_FOR_GENERATING_FLIGHT_ACCOMMODATION_BOOKINGS      =     (  ACCOMMODATION_BOOKINGS_PROCESSING_END_TIME    -      ACCOMMODATION_BOOKINGS_PROCESSING_START_TIME   )   *   1000




  if (EXECUTION_TIME_FOR_GENERATING_CUSTOMER_INFO > 1000) and (EXECUTION_TIME_FOR_GENERATING_CUSTOMER_INFO < 60000):
    root_logger.info(f'1. Execution time for generating CUSTOMER INFO : {EXECUTION_TIME_FOR_GENERATING_CUSTOMER_INFO} ms ({    round   (EXECUTION_TIME_FOR_GENERATING_CUSTOMER_INFO  /   1000, 2)   } secs) ')
    root_logger.info(f'')
    root_logger.info(f'')
  elif (EXECUTION_TIME_FOR_GENERATING_CUSTOMER_INFO >= 60000):
      root_logger.info(f'1. Execution time for generating CUSTOMER INFO :  {EXECUTION_TIME_FOR_GENERATING_CUSTOMER_INFO} ms  ({    round   (EXECUTION_TIME_FOR_GENERATING_CUSTOMER_INFO  /   1000, 2)   } secs)  ({   round  ((EXECUTION_TIME_FOR_GENERATING_CUSTOMER_INFO  /   1000) / 60, 4)     } mins)   ')
      root_logger.info(f'')
      root_logger.info(f'')
  else:
      root_logger.info(f'1. Execution time for generating CUSTOMER INFO :  {EXECUTION_TIME_FOR_GENERATING_CUSTOMER_INFO} ms ')
      root_logger.info(f'')
      root_logger.info(f'')



  if (EXECUTION_TIME_FOR_GENERATING_FLIGHT_SCHEDULES > 1000) and (EXECUTION_TIME_FOR_GENERATING_FLIGHT_SCHEDULES < 60000):
      root_logger.info(f'2. Execution time for generating FLIGHT SCHEDULES : {EXECUTION_TIME_FOR_GENERATING_FLIGHT_SCHEDULES} ms ({    round   (EXECUTION_TIME_FOR_GENERATING_FLIGHT_SCHEDULES  /   1000, 2)   } secs) ')
      root_logger.info(f'')
      root_logger.info(f'')
  elif (EXECUTION_TIME_FOR_GENERATING_FLIGHT_SCHEDULES >= 60000):
      root_logger.info(f'2. Execution time for generating FLIGHT SCHEDULES  {EXECUTION_TIME_FOR_GENERATING_FLIGHT_SCHEDULES} ms  ({    round   (EXECUTION_TIME_FOR_GENERATING_FLIGHT_SCHEDULES  /   1000, 2)   } secs)  ({   round  ((EXECUTION_TIME_FOR_GENERATING_FLIGHT_SCHEDULES  /   1000) / 60, 4)     } mins)   ')
      root_logger.info(f'')
      root_logger.info(f'')
  else:
      root_logger.info(f'2. Execution time for generating FLIGHT SCHEDULES  {EXECUTION_TIME_FOR_GENERATING_FLIGHT_SCHEDULES} ms ')
      root_logger.info(f'')
      root_logger.info(f'')

  

  if (EXECUTION_TIME_FOR_GENERATING_TICKET_PRICES > 1000) and (EXECUTION_TIME_FOR_GENERATING_TICKET_PRICES < 60000):
      root_logger.info(f'3. Execution time for generating TICKET PRICES : {EXECUTION_TIME_FOR_GENERATING_TICKET_PRICES} ms ({    round   (EXECUTION_TIME_FOR_GENERATING_TICKET_PRICES  /   1000, 2)   } secs) ')
      root_logger.info(f'')
      root_logger.info(f'')
  elif (EXECUTION_TIME_FOR_GENERATING_TICKET_PRICES >= 60000):
      root_logger.info(f'3. Execution time for generating TICKET PRICES:  {EXECUTION_TIME_FOR_GENERATING_TICKET_PRICES} ms  ({    round   (EXECUTION_TIME_FOR_GENERATING_TICKET_PRICES  /   1000, 2)   } secs)  ({   round  ((EXECUTION_TIME_FOR_GENERATING_TICKET_PRICES  /   1000) / 60, 4)     } mins)   ')
      root_logger.info(f'')
      root_logger.info(f'')
  else:
      root_logger.info(f'3. Execution time for generating TICKET PRICES:  {EXECUTION_TIME_FOR_GENERATING_TICKET_PRICES} ms ')
      root_logger.info(f'')
      root_logger.info(f'')



  if (EXECUTION_TIME_FOR_GENERATING_FLIGHT_BOOKINGS > 1000) and (EXECUTION_TIME_FOR_GENERATING_FLIGHT_BOOKINGS < 60000):
      root_logger.info(f'4. Execution time for generating FLIGHT BOOKINGS : {EXECUTION_TIME_FOR_GENERATING_FLIGHT_BOOKINGS} ms ({    round   (EXECUTION_TIME_FOR_GENERATING_FLIGHT_BOOKINGS  /   1000, 2)   } secs) ')
      root_logger.info(f'')
      root_logger.info(f'')
  elif (EXECUTION_TIME_FOR_GENERATING_FLIGHT_BOOKINGS >= 60000):
      root_logger.info(f'4. Execution time for generating FLIGHT BOOKINGS:  {EXECUTION_TIME_FOR_GENERATING_FLIGHT_BOOKINGS} ms  ({    round   (EXECUTION_TIME_FOR_GENERATING_FLIGHT_BOOKINGS  /   1000, 2)   } secs)  ({   round  ((EXECUTION_TIME_FOR_GENERATING_FLIGHT_BOOKINGS  /   1000) / 60, 4)     } mins)   ')
      root_logger.info(f'')
      root_logger.info(f'')
  else:
      root_logger.info(f'4. Execution time for generating FLIGHT BOOKINGS:  {EXECUTION_TIME_FOR_GENERATING_FLIGHT_BOOKINGS} ms ')
      root_logger.info(f'')
      root_logger.info(f'')
      


  if (EXECUTION_TIME_FOR_GENERATING_CUSTOMER_FEEDBACKS > 1000) and (EXECUTION_TIME_FOR_GENERATING_CUSTOMER_FEEDBACKS < 60000):
    root_logger.info(f'5. Execution time for generating CUSTOMER FEEDBACKS : {EXECUTION_TIME_FOR_GENERATING_CUSTOMER_FEEDBACKS} ms ({    round   (EXECUTION_TIME_FOR_GENERATING_CUSTOMER_FEEDBACKS  /   1000, 2)   } secs) ')
    root_logger.info(f'')
    root_logger.info(f'')
  elif (EXECUTION_TIME_FOR_GENERATING_CUSTOMER_FEEDBACKS >= 60000):
      root_logger.info(f'5. Execution time for generating CUSTOMER FEEDBACKS:  {EXECUTION_TIME_FOR_GENERATING_CUSTOMER_FEEDBACKS} ms  ({    round   (EXECUTION_TIME_FOR_GENERATING_CUSTOMER_FEEDBACKS  /   1000, 2)   } secs)  ({   round  ((EXECUTION_TIME_FOR_GENERATING_CUSTOMER_FEEDBACKS  /   1000) / 60, 4)     } mins)   ')
      root_logger.info(f'')
      root_logger.info(f'')
  else:
      root_logger.info(f'5. Execution time for generating CUSTOMER FEEDBACKS:  {EXECUTION_TIME_FOR_GENERATING_CUSTOMER_FEEDBACKS} ms ')
      root_logger.info(f'')
      root_logger.info(f'')
      


  if (EXECUTION_TIME_FOR_GENERATING_SALES_AGENTS > 1000) and (EXECUTION_TIME_FOR_GENERATING_SALES_AGENTS < 60000):
      root_logger.info(f'6. Execution time for generating SALES AGENTS : {EXECUTION_TIME_FOR_GENERATING_SALES_AGENTS} ms ({    round   (EXECUTION_TIME_FOR_GENERATING_SALES_AGENTS  /   1000, 2)   } secs) ')
      root_logger.info(f'')
      root_logger.info(f'')
  elif (EXECUTION_TIME_FOR_GENERATING_SALES_AGENTS >= 60000):
      root_logger.info(f'6. Execution time for generating SALES AGENTS:  {EXECUTION_TIME_FOR_GENERATING_SALES_AGENTS} ms  ({    round   (EXECUTION_TIME_FOR_GENERATING_SALES_AGENTS  /   1000, 2)   } secs)  ({   round  ((EXECUTION_TIME_FOR_GENERATING_SALES_AGENTS  /   1000) / 60, 4)     } mins)   ')
      root_logger.info(f'')
      root_logger.info(f'')
  else:
      root_logger.info(f'6. Execution time for generating SALES AGENTS:  {EXECUTION_TIME_FOR_GENERATING_SALES_AGENTS} ms ')
      root_logger.info(f'')
      root_logger.info(f'')
      


  if (EXECUTION_TIME_FOR_GENERATING_FLIGHT_DESTINATIONS > 1000) and (EXECUTION_TIME_FOR_GENERATING_FLIGHT_DESTINATIONS < 60000):
      root_logger.info(f'7. Execution time for generating FLIGHT DESTINATIONS : {EXECUTION_TIME_FOR_GENERATING_FLIGHT_DESTINATIONS} ms ({    round   (EXECUTION_TIME_FOR_GENERATING_FLIGHT_DESTINATIONS  /   1000, 2)   } secs) ')
      root_logger.info(f'')
      root_logger.info(f'')
  elif (EXECUTION_TIME_FOR_GENERATING_FLIGHT_DESTINATIONS >= 60000):
      root_logger.info(f'7. Execution time for generating FLIGHT DESTINATIONS:  {EXECUTION_TIME_FOR_GENERATING_FLIGHT_DESTINATIONS} ms  ({    round   (EXECUTION_TIME_FOR_GENERATING_FLIGHT_DESTINATIONS  /   1000, 2)   } secs)  ({   round  ((EXECUTION_TIME_FOR_GENERATING_FLIGHT_DESTINATIONS  /   1000) / 60, 4)     } mins)   ')
      root_logger.info(f'')
      root_logger.info(f'')
  else:
      root_logger.info(f'7. Execution time for generating FLIGHT DESTINATIONS:  {EXECUTION_TIME_FOR_GENERATING_FLIGHT_DESTINATIONS} ms ')
      root_logger.info(f'')
      root_logger.info(f'')
      


  if (EXECUTION_TIME_FOR_GENERATING_FLIGHT_PROMOS_AND_DEALS > 1000) and (EXECUTION_TIME_FOR_GENERATING_FLIGHT_PROMOS_AND_DEALS < 60000):
      root_logger.info(f'8. Execution time for generating FLIGHT PROMOS AND DEALS : {EXECUTION_TIME_FOR_GENERATING_FLIGHT_PROMOS_AND_DEALS} ms ({    round   (EXECUTION_TIME_FOR_GENERATING_FLIGHT_PROMOS_AND_DEALS  /   1000, 2)   } secs) ')
      root_logger.info(f'')
      root_logger.info(f'')
  elif (EXECUTION_TIME_FOR_GENERATING_FLIGHT_PROMOS_AND_DEALS >= 60000):
      root_logger.info(f'8. Execution time for generating FLIGHT PROMOS AND DEALS:  {EXECUTION_TIME_FOR_GENERATING_FLIGHT_PROMOS_AND_DEALS} ms  ({    round   (EXECUTION_TIME_FOR_GENERATING_FLIGHT_PROMOS_AND_DEALS  /   1000, 2)   } secs)  ({   round  ((EXECUTION_TIME_FOR_GENERATING_FLIGHT_PROMOS_AND_DEALS  /   1000) / 60, 4)     } mins)   ')
      root_logger.info(f'')
      root_logger.info(f'')
  else:
      root_logger.info(f'8. Execution time for generating FLIGHT PROMOS AND DEALS:  {EXECUTION_TIME_FOR_GENERATING_FLIGHT_PROMOS_AND_DEALS} ms ')
      root_logger.info(f'')
      root_logger.info(f'')
      


  if (EXECUTION_TIME_FOR_GENERATING_FLIGHT_TICKET_SALES > 1000) and (EXECUTION_TIME_FOR_GENERATING_FLIGHT_TICKET_SALES < 60000):
      root_logger.info(f'9. Execution time for generating FLIGHT TICKET SALES : {EXECUTION_TIME_FOR_GENERATING_FLIGHT_TICKET_SALES} ms ({    round   (EXECUTION_TIME_FOR_GENERATING_FLIGHT_TICKET_SALES  /   1000, 2)   } secs) ')
      root_logger.info(f'')
      root_logger.info(f'')
  elif (EXECUTION_TIME_FOR_GENERATING_FLIGHT_TICKET_SALES >= 60000):
      root_logger.info(f'9. Execution time for generating FLIGHT TICKET SALES:  {EXECUTION_TIME_FOR_GENERATING_FLIGHT_TICKET_SALES} ms  ({    round   (EXECUTION_TIME_FOR_GENERATING_FLIGHT_TICKET_SALES  /   1000, 2)   } secs)  ({   round  ((EXECUTION_TIME_FOR_GENERATING_FLIGHT_TICKET_SALES  /   1000) / 60, 4)     } mins)   ')
      root_logger.info(f'')
      root_logger.info(f'')
  else:
      root_logger.info(f'9. Execution time for generating FLIGHT TICKET SALES:  {EXECUTION_TIME_FOR_GENERATING_FLIGHT_TICKET_SALES} ms ')
      root_logger.info(f'')
      root_logger.info(f'')
      


  if (EXECUTION_TIME_FOR_GENERATING_FLIGHT_ACCOMMODATION_BOOKINGS > 1000) and (EXECUTION_TIME_FOR_GENERATING_FLIGHT_ACCOMMODATION_BOOKINGS < 60000):
      root_logger.info(f'10. Execution time for generating ACCOMMODATION BOOKINGS : {EXECUTION_TIME_FOR_GENERATING_FLIGHT_ACCOMMODATION_BOOKINGS} ms ({    round   (EXECUTION_TIME_FOR_GENERATING_FLIGHT_ACCOMMODATION_BOOKINGS  /   1000, 2)   } secs) ')
      root_logger.info(f'')
      root_logger.info(f'')
  elif (EXECUTION_TIME_FOR_GENERATING_FLIGHT_ACCOMMODATION_BOOKINGS >= 60000):
      root_logger.info(f'10. Execution time for generating ACCOMMODATION BOOKINGS:  {EXECUTION_TIME_FOR_GENERATING_FLIGHT_ACCOMMODATION_BOOKINGS} ms  ({    round   (EXECUTION_TIME_FOR_GENERATING_FLIGHT_ACCOMMODATION_BOOKINGS  /   1000, 2)   } secs)  ({   round  ((EXECUTION_TIME_FOR_GENERATING_FLIGHT_ACCOMMODATION_BOOKINGS  /   1000) / 60, 4)     } mins)   ')
      root_logger.info(f'')
      root_logger.info(f'')
  else:
      root_logger.info(f'10. Execution time for generating ACCOMMODATION BOOKINGS:  {EXECUTION_TIME_FOR_GENERATING_FLIGHT_ACCOMMODATION_BOOKINGS} ms ')
      root_logger.info(f'')
      root_logger.info(f'')


  
  root_logger.debug("Successfully completed generating data")
  root_logger.debug("")
  root_logger.debug("")
  root_logger.debug("Terminating data generation job...")
  root_logger.debug("Session ended.")
      

generate_travel_data()