import string
import random

# Secure password generator project
# Required optional arguments for the function

# The values of below arguments should be a string
# upper_case="yes/no"
# lower_case="yes/no"
# numeric_case="yes/no"
# punctuations_case="yes"

# The value of password length should be an integer
# password_length=12

# Default values
# upper_case="yes"
# lower_case="yes"
# numeric_case="yes"
# punctuations_case="yes"
# password_length=12

# Sample command line usage
# password_generator = SPG()
# my_password = password_generator.password_brew()
# print(my_password)

# We can use the below mentioned arguments as and when required along with the Class declaration.
# upper_case="yes"
# lower_case="yes"
# numeric_case="yes"
# punctuations_case="yes"
# password_length=12

# password_generator = SPG(upper_case="no",lower_case="no",numeric_case="no")
# my_password = password_generator.password_brew()
# print(my_password)


class SPG:
        def __init__(self,upper_case="yes",lower_case="yes",numeric_case="yes",punctuations_case="yes",password_length=12):
            self.upper_case = upper_case
            self.lower_case = lower_case
            self.numeric_case = numeric_case
            self.punctuations_case = punctuations_case
            self.password_length = password_length
        def password_brew(self):
                password_length = self.password_length
                upper_case = self.upper_case
                lower_case = self.lower_case
                numeric_case = self.numeric_case
                punctuations_case = self.punctuations_case

                # Listout the upper,lower,punctuations characters to a list
                upper_case_array = string.ascii_uppercase.upper()
                lower_case_array = string.ascii_lowercase.lower()
                punctuation_case_array = list(string.punctuation)

                # Select 0-9 integer range
                numeric_range = 10
                upper_case_string = ""
                lower_case_string = ""
                numeric_string = ""
                punctuation_string = ""

                # The loop will execute exponent to 2 of the password length
                i = 0
                while i < (password_length*password_length):
                    if upper_case == "yes":
                        upper_case_index = random.randrange(len(upper_case_array))
                        upper_case_string += upper_case_array[upper_case_index]
                    elif upper_case == "no":
                        pass
                    else:
                        pass
                    if lower_case == "yes":
                        lower_case_index = random.randrange(len(lower_case_array))
                        lower_case_string += lower_case_array[lower_case_index]
                    elif lower_case == "yes":
                        pass
                    else:
                        pass
                    if numeric_case == "yes":
                        numeric_case_array = random.randrange(numeric_range)
                        numeric_string += str(numeric_case_array)
                    if punctuations_case == "yes":
                        string_punctuations = random.randrange(len(punctuation_case_array))
                        punctuation_string += str(punctuation_case_array[string_punctuations])
                    elif punctuations_case == "no":
                        pass
                    else:
                        pass
                    i += 1
                # It will form a lengthy password elements in the array
                password_list = list(upper_case_string + lower_case_string + numeric_string + punctuation_string)

                # The elements in the array will be shuffled
                random.shuffle(password_list)

                # From the shuffled elements, randomly picked characters will be added to another array.
                # The length of this new array will be equal to the length of the password
                password_string = random.choices(password_list,k=password_length)

                # All elements in teh array will be joined to a string
                password = ''.join(password_string)

                # The newly generated password will be pickled with the function
                return(password)

