from agents import Agent

# For simple lists
agent_with_list_output = Agent(
   name="List Generator",
   instructions="Generate lists of items based on the user's request.",
   output_type=list[str],  # Returns a list of strings
)

# For dictionaries
agent_with_dict_output = Agent(
   name="Dictionary Generator",
   instructions="Create key-value pairs based on the input.",
   output_type=dict[
       str, int
   ],  # Returns a dictionary with string keys and integer values
)

# For simple primitive types
agent_with_bool_output = Agent(
   name="Decision Maker",
   instructions="Answer yes/no questions with True or False.",
   output_type=bool,  # Returns a boolean
)