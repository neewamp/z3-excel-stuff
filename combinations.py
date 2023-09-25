def combinationsNoOrder(n: int, things=[True,False]) -> list[list[bool]]:
    if n == 0:
        return [[]]
    # Solve the problem recursively for smaller n
    prev_answers = combinationsNoOrder(n - 1, things)
    answer = []
    
    # Using each of the lists of size n-1 we need to make the new lists of combinations of size n
    # All this entails is append the two additional options to the previous answers 
    # for example [True, True] is one combination that can be used to generate two additional combinations of size 3:
    #  [True, True, True] and [False, True, True]
    for i in range(len(prev_answers)):
        # in vba the `+` operator is going to be something wonky and 
        # you need to be careful to make a copy of the prev_answers and not modify it when constructing this new array
        for thing in things: 
            answer.append([thing] + prev_answers[i])
    return answer


# What are all list of true and false that are length 3
# for i in (combinationsNoOrder(2, ["true", "false", "unknown"])): 
#    print(i)