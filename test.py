def main():
    memo = {}

    # Gets all the probabilities that would occur from moving from this state to another state
    def get_curr_probs(p_one_num: int, p_one_score: int, p_two_num: int, p_two_score: int) -> dict:
        curr_probs = {}

        for i in range(p_one_num + 1, 13):
            key = (p_two_num, p_two_score, i, p_one_score + 1)
            if key not in memo:
                memo[key] = prob_of_win(p_two_num, p_two_score, i, p_one_score + 1)
            curr_probs[i] = (probs[i] / 36 *
                             (1 - memo[key]))
        return curr_probs

    probs = {
        1: 0,
        2: 1,
        3: 2,
        4: 3,
        5: 4,
        6: 5,
        7: 6,
        8: 5,
        9: 4,
        10: 3,
        11: 2,
        12: 1
    }

    sum_probs = {
        1: 0,
        2: 1,
        3: 3,
        4: 6,
        5: 10,
        6: 15,
        7: 21,
        8: 26,
        9: 30,
        10: 33,
        11: 35,
        12: 36
    }

    # gets prob of win assuming you take every number possible
    def prob_of_win(p_one_num: int, p_one_score: int, p_two_num: int, p_two_score: int) -> float:
        if max(p_one_num, p_two_num) == 12:
            if max(p_one_score, p_two_score) >= 5:
                if p_one_score > p_two_score:
                    return 1
                elif p_one_score == p_two_score:
                    return .5
                else:
                    return 0
            else:
                return int(not p_one_num == 12)

        # array of probabilities for me moving to a different state
        my_probs = get_curr_probs(p_one_num, p_one_score, p_two_num, p_two_score)

        # array of probabilities for an opponent moving to a different state
        opp_probs = get_curr_probs(p_two_num, p_two_score, p_one_num, p_one_score)

        # sum over all my probs
        total = 0
        for i in my_probs.keys():
            total = total + my_probs[i]

        # sum over all opp probs
        opp_total = 0
        for j in opp_probs.keys():
            opp_total = opp_total + opp_probs[j]
        opp_total = sum_probs[p_one_num] / 36 * (1 - opp_total)
        total = total + opp_total

        # now all thats left to consider is the remainder term which is equivalent to
        # the original term
        total = total - sum_probs[p_two_num] * sum_probs[p_one_num] / (36 ** 2)
        total = total * ((1 - sum_probs[p_two_num] * sum_probs[p_one_num] / (36 ** 2)) ** (-1))
        return total

    for j in range(3, 13):
        print(j, 1 - prob_of_win(2, 1, j, 2))
    print(1, 1 - prob_of_win(2, 1, 2, 1))
    print(prob_of_win(1, 3, 11, 1))


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main()
