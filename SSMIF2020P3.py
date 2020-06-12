#---------------------------------------------------------------------------------
#   Agatha Malinowski 
#---------------------------------------------------------------------------------

#---------------------------------------------------------------------------------
#
#   Load all dependencies
#
#---------------------------------------------------------------------------------
import copy


#---------------------------------------------------------------------------------
#
# flat_list: Function
#
# Parameters: 
#   vlist: list of numbers
#
#   Perform basic calculation on a given nested list; The function returns 
#   a flat list containting numbers calucated following predefined criteria
#   listed below. 
#
#   [1] If the index of an inner-list is even, you must ​double ​ all values 
#   starting from (and including) the ​first​ occurrence of the number 9 
#   in that list all the way to (and including) the ​next​ occurrence of 
#   the number 6 in the remainder of that list
#
#   [2] If the index of an inner list is odd, you must ​triple ​ all the 
#   values starting from (and including) the ​first ​occurrence of the number 7 
#   in that list all the way to (and including) the ​next ​occurrence of 
#   the number 4 in the remainder of that list. 
#--------------------------------------------------------------------------------
def flat_list(vlist):
    sum = 0 # sum of items calulated following the special requirments. 
    rsum = 0 # regular sum of items ([1] + [2]+ [3] ...)
    cnt = 0 # inner list's counter
    flist = [] # flatened list
    scase = False # special case tracker
    
    while cnt < len(vlist): # iterate through inner lists
        sum = 0  # reset list's sum special calculation
        rsum = 0 # reset list's sum normal calculation
        if (len(vlist[cnt])-1) % 2 == 0: # check if list's index is even or odd?
            for x in vlist[cnt]:  # index is even
                rsum = rsum + x
                if x == 9: scase = True  # turn on special case tracker
                if scase == True:
                    sum = sum + (x * 2) # double the list value at the index and add to the sum
                else: sum = sum + x
                if x == 6: scase = False # Turn OFF special case marker
        else: 
            for x in vlist[cnt]: # list's index is odd
                rsum = rsum + x
                if x == 7: scase = True #turn on special case tracker
                if scase == True:
                    sum = sum + (x * 3) # triple the list value at the index and add to the sum
                else: sum = sum + x
                if x == 4: scase = False # Turn OFF special case marker
        
        # Build the new lsit based on the calculated results
        if scase == True: flist.append(rsum)    # if special case tracker was not truned off append simple sum of items
        else: flist.append(sum) # Special case tracker is off;
        cnt = cnt + 1 # Increment loops counter
    return flist
#--------------------------------------------------------------------------------
#   End of flat_list
#--------------------------------------------------------------------------------

#---------------------------------------------------------------------------------
#
# sum_ssmif: Function
#
# Parameters: 
#   vlist list of numbers
#
#   Perform basic calculation following predefined criteria;
#
#   [1] Then, once a single list of values which were obtained 
#   from each inner-list, ​ignore any values in that list starting 
#   from (and including) the ​first​ occurrence of the number 4 all the way 
#   to (and including) the ​next​ occurrence of the number 5 in the remainder 
#   of the list. 
#
#   [2] If there is no end marker (6, 4, 5) after a start marker (9, 7, 4), 
#   return the normal sum of the list. 
#--------------------------------------------------------------------------------
def sum_ssmif(vlist):
    cnt = 0 # Loop counter
    scase = False # Special cases tracker

    # Flatten the nested list and perform the requiried calculations
    flist = flat_list(vlist) 
    # Create a copy of the flat list to handle special cases
    flistb = copy.deepcopy(flist)
    print("Simplifies to: ", flist)

    # perform the requiried calculations
    while cnt < len(vlist):
        if flistb[cnt] == 4: scase = True  # START special case marker identified
        if scase == True:   # Special case ON
            flist[cnt] = 0  # Assign zero to the corresponding list item
        if flistb[cnt] == 5: scase = False  # END of special case marker found
        cnt = cnt + 1   # Increment loop counter

    if scase == True: 
        print("Simplifies to: ", flistb)
        return sum(flistb)  # If special case marker is still ON return sum of the original list items
    else: 
        print("Simplifies to: ", flist)
        return sum(flist) # If special case marker is OFF return sum of the calculated list items
#--------------------------------------------------------------------------------
#   End of flat_list
#--------------------------------------------------------------------------------

#----------------------------------------------------------------------------
# Main program 
# ----------------------------------------------------------------------------

# Test case list
my_list = [[1, 2, 3, 9, 2, 6, 1], [1, 3], [1, 2, 3], [7, 1, 4, 2], [1, 2, 2]]

print("")
print("Input: ", my_list)

# Perform calculations
my_sum = sum_ssmif(my_list)
# Print results
print("Simplified output: ", my_sum)
