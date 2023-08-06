def help():
    print("Welcome to Quito!")
    print("\n")
    print("You can provide the root of the configuration to run quito.")
    print("Here is the template of the configuration file.")

    template = '''
[program]
root= 
;(Required)
;Description: The absolute root of your quantum program file.
num_qubit= 
;(Required)
;Description: The total number of qubit of your quantum program.
inputID= 
;(Required)
;Description: The ID of input qubits.
outputID= 
;(Required)
;Description: The ID of output qubits which are the qubits to be measured.
;Format: A non-repeating sequence separated by commas.

[quito_configuration]
coverage_criterion= 
;Description: The coverage criterion you choose.
;Choice: IC/OC/IOC
K= 
;(Optional)
;Description: The total number of test suites, K=200 by default.
M= 
;(Optional)
;Description: The number of test suite groups, M=20 by default.
BUDGET= 
;(Optional)
;Description: The budget of the number of test cases in one test suite, BUDGET=10*number of inputs by default.
confidence_level= 
;(Optional)
;Description: The confidence level for statistical test, confidence_level=0.01 by default.
statistical_test= 
;(Optional)
;Description: The statistical test for assessment, statistical_test=one-sample Wilcoxon signed rank test by default.

[program_specification_category]
ps_category= 
;(Required) Description: The category of your program specification. (full/partial/no)

[program_specification]
;(Required for full and partial program specification)
;Description: The program specification.
;Format:input string,output string=probability
'''
    print(template)
    print('\n')

    print("Here is the example of the configuration file and the quantum program file.")

    example = '''
[program]
root=SWAP.py
num_qubit=3
inputID=0,1
outputID=2

[program_specification_category]
ps_category=full

[quito_configuration]
coverage_criterion=IC
K=200
M=10
BUDGET=20
confidence_level=0.01
statistical_test=one-sample Wilcoxon signed rank test    

[program_specification]
01,1=0.5
01,0=0.5
00,1=1
11,1=1
10,1=0.5
10,0=0.5
    '''
    program = '''
def run(qc):
    qc.h(2)
    qc.cswap(2,0,1)
    qc.h(2)
    qc.x(2)

    qc.measure(2,0)
    '''
    print(example)
    print("Here is the example of the quantum program file.")
    print(program)

if __name__ == '__main__':
    help()