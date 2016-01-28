-- This is a Forth interpreter

import Data.HashMap.Strict as H

-- Initial types

type ForthState = (IStack, CStack, Dictionary)

type IStack = [Integer]
initialIStack = []

type CStack = [[String]]
initialCStack = []

-- Type for the symbol dictionary

type Dictionary = H.HashMap String [Entry]

data Entry =
     Prim ([Integer] -> [Integer])
   | Def [String]
   | Num Integer
   | Unknown String


-- Printing

instance Show Entry where
  show (Prim f)    = "Prim"
  show (Def s)     = show s
  show (Num i)     = show i
  show (Unknown s) = "Unknown: " ++ s

-- Dictionary helpers

wrap2 f (x:y:xs) = (f x y):xs
wrap2 f _ = error "Value stack underflow!"

wrap3 f (x:y:xs) = (f y x):xs
wrap3 f _ = error "Value stack underflow!"


dlookup :: String -> Dictionary -> Entry
dlookup word dict =
  case H.lookup word dict of
    Nothing -> case reads word of
                 [(i,"")] -> Num i
                 _        -> Unknown word
    Just x  -> head x

dinsert :: String -> Entry -> Dictionary -> Dictionary
dinsert key val dict =
   case H.lookup key dict of
      Nothing -> H.insert key [val] dict
      Just x  -> H.insert key (val:x) dict

-- Initial Dictionary

initialDList = [("+", wrap2 (+)),
               ("-", wrap3 (-)),
               ("*", wrap2 (*)),
               ("/", wrap3 (div)),
               ("dup", dup),
               ("swap", swap),
               ("drop", drp),
               ("rot", rot),
               ("<", compop1),
               (">", compop2)]

-- Helper Functions for initialDList
dup [] = []
dup (x:xs) = (x:x:xs)

swap [] = []
swap (x:(y:ys)) = (y:(x:ys))

drp [] = []
drp (x:xs) = xs

rot [] = []
rot (x:xs) = ((last xs):x:(init xs))

compop1 (x:y:z) 
  | y < x = (-1):z
  | otherwise = 0:z

compop2 (x:y:z) 
  | y > x = (-1):z
  | otherwise = 0:z

dictionary = foldl (\x (y,z) -> dinsert y (Prim z) x) H.empty initialDList

sepElse s = if ((dropWhile (/= "else") s) == [])
                                then takeWhile (/= "else") s 
                                else (takeWhile (/= "else") s) ++ (tail (dropWhile (/= "then") s))
sepThen s = if ((dropWhile (/= "else") s) == [])
               then []
               else (init (tail (dropWhile (/= "else") s))) ++ (tail (dropWhile (/= "then") s))

sepAgain s = takeWhile (/= "again") s ++ ["again"]
sepExit s = if ((dropWhile (/= "again") s) == [])
               then []
               else tail (dropWhile (/= "again") s)
          
-- The Evaluator

eval :: [String] -> ForthState -> IO ForthState
eval []    (istack, [],     dict) = return (istack, [], dict)
eval words (istack, cstack, dict) =
  case dlookup (head words) dict of
    Num i        -> eval xs (i:istack, cstack, dict)
    Prim f       -> eval xs (f istack, cstack, dict)
    Def s -> eval (s ++ xs) (istack, cstack, dict)
    Unknown "begin" -> eval xs (istack, ((sepAgain xs):cstack), dict)
    Unknown "again" -> eval (head cstack ++ xs) (istack, cstack, dict)
    Unknown "exit" -> eval (sepExit xs) (istack, tail cstack, dict)
    Unknown "if" -> if (head istack == -1)
                           then eval (sepElse xs) (tail istack, cstack, dict)
                           else eval (sepThen xs) (tail istack, cstack, dict)
    Unknown ":" -> let fn = head xs
                       args = init (tail xs)
                    in if ((last xs) == ";")
                          then eval args (istack, cstack, (dinsert fn (Def args) dict))
                          else error "Function error."
    Unknown ".S" -> do {putStrLn $ show $ reverse istack;
                       eval xs (istack, cstack, dict)}
    Unknown "."  -> do { putStrLn $ show (head istack);
                             eval xs (tail istack, cstack, dict) }
    Unknown _ -> error "Unknown word."
  where xs = tail words

repl :: ForthState -> IO ForthState
repl state =
  do putStr "> " ;
     input <- getLine
     nustate <- eval (words input) state
     repl nustate

main = do
  putStrLn "Welcome to your forth interpreter!"
  repl (initialIStack, initialCStack, dictionary)
