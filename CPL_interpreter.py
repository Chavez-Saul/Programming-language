""" Class Lexicon
    This class will store information of the buffer and the stack."""
class lexicon:

        
        def __init__(self, token):
                self.token = list()
                self.token.extend(token)
                self.index = -1
                self.stack = list()

        ## get(): void
        ## get(self) will consume the current token
        def get(self):
                if(self.index < len(self.token) -1):
                        self.index += 1
                return self.token[self.index]
        
        ## current_token: list X L -> L
        ## current_token will return the literal in
        ## the current index position
        def current_token(self):
            return self.token[self.index]

        ## push: Stack X L -> Stack
        ## push(self, literal) "pushes" the current literal
        ## onto the stack
        def push(self, literal):
                self.stack.append(literal)

## IT_Tail_Selection_Set: char -> bool
## checks to see if lex is in the selection set for IT_Tail
def IT_Tail_Selection_Set(lex):
        return lex in ".)"

## AT_Tail_Selection_Set: char -> bool
## checks to see if lex is in the selection set for AT_Tail
def AT_Tail_Selection_Set(lex):
        return lex in "v->.)"

## OT_Tail_Selection_Set: char -> bool
## checks to see if lex is in the selection set for OT_Tail
def OT_Tail_Selection_Set(lex):
        return lex in "->.)"

## boolean_connective_and: char X char -> bool
## Will determine wheiter to return a true or a false value
def boolean_connective_and(literal1, literal2):
        if literal1 == 'F' or literal2 == 'F':
                return 'F'
        else:
                return 'T'

## boolean_connective_or: char X char -> bool
## Will determine wheiter to return a true or a false value
def boolean_connective_or(literal1, literal2):
        if literal1 == 'F' and literal2 == 'F':
                return 'F'
        else:
                return 'T'

## boolean_connective_imply: char X char -> bool
## Will determine wheiter to return a true or a false value
def boolean_connective_imply(literal1, literal2):
        if literal1 == 'T' and literal2 == 'F':
                return 'F'
        else:
                return 'T'  

## B : Bool stmt
def B(lex):
        lex.get()
        if IT(lex):
                if lex.current_token() == '.':
                        print(lex.stack.pop())
                        lex.get()
                        return True
                else:
                        return False
        else:
                
                return False
    
## IT : Imply term
def IT(lex):
    if OT(lex):
        if IT_Tail(lex):
                return True
        else:
            return False
    else:
        return False
    
## IT_Tail : Imply tail
def IT_Tail(lex):
        if lex.current_token() == '-':
                lex.get()
                if lex.current_token() == '>':
                        lex.get()
                        if OT(lex):
                                if IT_Tail(lex):
                                        l1 = lex.stack.pop()
                                        l2 = lex.stack.pop()
                                        lex.push(boolean_connective_imply(l2,l1))
                                        return True
                                else:
                                        return False
                        else:
                                return False
                else:
                        print("Error: Was expecting \"->\" but got \"%s\" ." % lex.current_token())
                        return False
        elif IT_Tail_Selection_Set(lex.current_token()):
                return True
        else:
                print("Error: Was expecting an \".\" or \")\" but got a \"%s\"." % lex.current_token())
                return False
    
## OT : Or term
def OT(lex):
        if AT(lex):
                if OT_Tail(lex):
                    return True
                else:
                    return False
        else:
                
                return False
    
## O_Tail : Or tail
def OT_Tail(lex):

        if lex.current_token() == 'v':
                lex.get()
                if AT(lex):
                        if OT_Tail(lex):
                                l1 = lex.stack.pop()
                                l2 = lex.stack.pop()
                                lex.push(boolean_connective_or(l1,l2)) 
                                return True
                        else:
                                return False
                else:
                        return False

        elif OT_Tail_Selection_Set(lex.current_token()):
                return True
        else:
                print("Error: Was expecting an \".\", \")\", \"->\" or \"^\" but got a %s" % lex.current_token())
                return False

## AT : And term
def AT(lex):
        if L(lex):
                if AT_Tail(lex):
                        return True
                else:
                        
                        return False
        else:
                return False

## AT_Tail : And tail
def AT_Tail(lex):
        if lex.current_token() == '^':
                lex.get()
                if L(lex):
                        if AT_Tail(lex):
                                l1 = lex.stack.pop()
                                l2 = lex.stack.pop()
                                lex.push(boolean_connective_and(l1,l2))                      
                                return True
                        else:
                                return False
                else:
                        return False

        elif AT_Tail_Selection_Set(lex.current_token()):
                return True
        else:
                print("Error: Was expecting an \".\", \")\", \"->\" or \"v\" but got a %s" % lex.current_token())
                return False




## L : Literal
def L(lex):
        if A(lex):
                return True

        elif lex.current_token() == '~':
                
                lex.get()
                if L(lex):
                        if lex.stack.pop() == 'T':
                                lex.push('F')
                        else:
                                lex.push('T')
                        return True
                else:
                        return False
        else:
                return False

## A : Atom
def A(lex):
        
        if lex.current_token() == '(':
                lex.get()
                if IT(lex):
                    if lex.current_token() == ')':
                        lex.get()
                        return True
                    else:
                        return False
                else:
                    return False
        elif lex.current_token() == 'T':
                lex.push(lex.current_token())
                lex.get()
                return True
        elif lex.current_token() == 'F':
                lex.push(lex.current_token())
                lex.get()
                return True
        else:
                print("Error: Was expecting a literal but got a \"%s\"." % lex.current_token())
                return False
        
def main():
        
        MyX = input("Prompt ")
        MyLex = lexicon(MyX)
        B(MyLex)
            
if __name__ == "__main__":
    main()
