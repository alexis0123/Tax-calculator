import os

class Tax:
    def __init__(self, income, deduction=0):
        self.income = income
        self.deduction = deduction
        self.annual_bracket = [
        {"base":8000000, "add":2202500, "rate":0.35},
        {"base":2000000, "add":402500, "rate":0.30},
        {"base":800000, "add":102500, "rate":0.25},
        {"base":400000, "add":22500, "rate":0.20},
        {"base":250000, "add":0, "rate":0.15}
        ]

    def compute(self, type):

        bracket = self.annual_bracket

        if type == "standard" or type == "itemized":
            deduction = self.deduction
        elif type == "osd":
            deduction = self.income * 0.40
        else:
            raise TypeError("compute Type doesnt exist")
        
        income = self.income
        gross = income - deduction

        for rate in bracket:
            if gross > rate["base"]:
                net = gross - rate["base"]
                tax = net * rate["rate"]
                total = tax + rate["add"]

                return {
                "income": income,
                "deduction": deduction,
                "gross": gross,
                "base": rate["base"],
                "net": net,
                "rate": rate["rate"],
                "tax": tax,
                "add": rate["add"],
                "total": total
                }
        raise ValueError("gross is not taxable")
    
    
def setting():
    available_type = ["standard", "osd", "itemized"]
    while True:
        try:
            type = input("Ctrl + D to Exit\nStandard, Itemized, or OSD: ").strip().lower()
            if type not in available_type:
                continue
            try:
                decimal = int(input("How many decimal places: "))
            except ValueError:
                continue
        except EOFError:
            raise EOFError
        return type, decimal
    

def get_income(type,decimal):
    monthly = False
    while True:
        try:
            income = input("Ex. 200,000 and 200000 monthly\nIncome: ").strip().replace(",", "")
            if type == "itemized":
                try:
                    deduction = input("Deduction: ").strip().replace(",", "")
                except ValueError:
                    continue

                if "monthly" in deduction:
                    deduction = float(deduction.replace("monthly", "")) * 12
                else:
                    try:
                        deduction = float(deduction)
                    except ValueError:
                        continue
            else:
                deduction = 0
        except EOFError:
            raise EOFError

        if "monthly" in income:
            income = float(income.replace("monthly", "")) * 12
            monthly = True
        else:
            try:
                income = float(income)
            except ValueError:
                continue

        return income, deduction, monthly


def main():
    while True:
        try:
            type, decimal = setting()
        except EOFError:
            break

        while True:
            os.system("clear")
            try:
                income, deduction, monthly = get_income(type,decimal)
            except EOFError:
                break
            tax = Tax(income, deduction)

            #income x 12
            if monthly:
                print(f"\n{income/12:,.{decimal}f} x 12 = {income:,.{decimal}f}\n")

            #Income
            print(f"\n   {income:,.{decimal}f} Annual Income")

            #Deduction
            if type == "itemized":
                print(f"-  {deduction:,.{decimal}f}")
            elif type == "osd":
                deduction = income * 0.40
                print(f"-  40% ({deduction:,.{decimal}f})")

            try:
                sol = tax.compute(type)
            except ValueError:
                print(f"{"-"*25}\n   {income - deduction:,.{decimal}f} is not taxable")
                #This prompts the user to press enter for another entry
                try:
                    x = input()
                except EOFError:
                    break
                continue

            #Displays the rest of steps
            
            #Gross
            if type != "standard":
                print(f"{"-"*25}\n   {sol["gross"]:,.{decimal}f}")

            #Base
            print(f"-  {sol["base"]:,.{decimal}f}")

            #Net
            print(f"{"-"*25}\n   {sol["net"]:,.{decimal}f}")

            #Rate
            print(f"x  {sol["rate"]*100:.0f}%")

            #Tax
            print(f"{"-"*25}\n   {sol["tax"]:,.{decimal}f}")

            #Additional
            if sol["add"] != 0:
                print(f"+  {sol["add"]:,.{decimal}f}")

            #Total tax
            print(f"{"-"*25}\n   {sol["total"]:,.{decimal}f} Total Annual Tax\n")

            #Monthly Tax (x/12)
            print(f"Monthly Tax:  {sol["total"]:,.{decimal}f} / 12 = {sol["total"]/12:,.{decimal}f}")

            #This prompts the user to press enter for another entry
            try:
                x = input()
            except EOFError:
                break

if __name__ == "__main__":
    main()
