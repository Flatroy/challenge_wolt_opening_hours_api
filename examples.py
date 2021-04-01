example_input = """{
   "monday":[
      
   ],
   "tuesday":[
      {
         "type":"open",
         "value":36000
      },
      {
         "type":"close",
         "value":64800
      }
   ],
   "wednesday":[
      
   ],
   "thursday":[
      {
         "type":"open",
         "value":36000
      },
      {
         "type":"close",
         "value":64800
      }
   ],
   "friday":[
      {
         "type":"open",
         "value":36000
      }
   ],
   "saturday":[
      {
         "type":"close",
         "value":3600
      },
      {
         "type":"open",
         "value":36000
      }
   ],
   "sunday":[
      {
         "type":"close",
         "value":3600
      },
      {
         "type":"open",
         "value":43200
      },
      {
         "type":"close",
         "value":75600
      }
   ]
}
"""

example_output = """Monday: Closed
Tuesday: 10 AM - 6 PM
Wednesday: Closed
Thursday: 10 AM - 6 PM
Friday: 10 AM - 1 AM
Saturday: 10 AM - 1 AM
Sunday: 12 PM - 9 PM"""
