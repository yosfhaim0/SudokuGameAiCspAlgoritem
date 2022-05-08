import copy

import CSProblem


# jupyter
def solve(n):
    p = backtrack(CSProblem.create())
    CSProblem.present(p)


def backtrack(p):
    # תמצא את התא הבא שכדאי למלא אותו בערך
    var = next_var(p)  #
    if var == None:
        return p
    # var= next ceil to treatment
    dom = sorted_domain(p, var, LCV=True)  #
    # lcv= least constrianing value
    # סדר את הדומיין ככה שהראשון יהיה הכי כדאי לבחור.
    for i in dom:
        bu = copy.deepcopy(p)
        CSProblem.assign_val(bu, var, i)
        propagate_constraints(bu, var)  #
        bu = backtrack(bu)
        # במצב שבו מילאתי תא
        # בצורה לא נכונה יווצר מצב בו הדומיין של תא מסויים ריק אבל התא ריק
        # וזה אומר שהלוח במצב הנוכחי לא יכול להיפתר לכן צריך לחזור אחורה
        if CSProblem.is_solved(bu):
            return bu
    return p


def sorted_domain(p, var, LCV=True):
    if LCV == False:
        return CSProblem.domain(p, var)
    l = []
    for i in CSProblem.domain(p, var):
        l += [[p, var, i]]
    sd = []
    for i in sorted(l, key=num_of_del_vals):
        sd += [i[2]]
    return sd


# כמה אני יצטרך למחוק מדומיינים של תאים אחרים אם אני יציב ערך בתא שבחרתי
def num_of_del_vals(l):
    # l=[problem, the variable, the val. assigned to the var.]
    # returns the num. of vals. erased from vars domains after assigning x to v
    count = 0
    for inf_v in CSProblem.list_of_influenced_vars(l[0], l[1]):
        for i in CSProblem.domain(l[0], inf_v):
            if not CSProblem.is_consistent(l[0], l[1], inf_v, l[2], i):
                count += 1
    return count


# מחזיר את המיקום הבא על הלוח שכדאי למלא
def next_var(p, MRV=True):
    # minimum reimining value
    # Returns next var. to assign
    # If MRV=True uses MRV heuristics
    # If MRV=False returns first non-assigned ver.
    if MRV == False:
        v = CSProblem.get_list_of_free_vars(p)
        if v == []:
            return None
        else:
            return v[0]
    # if mrv==true:
    # find the value whit minimum domain size
    m = float("inf")
    mrv = None
    for i in CSProblem.get_list_of_free_vars(p):
        ds = CSProblem.domain_size(p, i)
        if ds < m:
            m = ds
            mrv = i
    return mrv


# לאחר הצבת ערך אנחנו רוצים להפיץ את האילוצים לכל מי שמושפע על ידינו
def propagate_constraints(p, v):
    for i in CSProblem.list_of_influenced_vars(p, v):
        for x in CSProblem.domain(p, i):
            if not CSProblem.is_consistent(p, i, v, x, CSProblem.get_val(p, v)):
                CSProblem.erase_from_domain(p, i, x)


if __name__ == "__main__":
    solve(3)
