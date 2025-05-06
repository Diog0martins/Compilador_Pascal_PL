program FloatExample;

var
  num1, num2, sum, difference, product, quotient: Real;

begin
  { Assigning values to the variables }
  num1 := 5.25;
  num2 := 3.75;
(* This is a multi-line comments
   and it will span multiple lines. *)

{ This is a single line comment in pascal }
  { Performing arithmetic operations }
  sum := num1 + num2;
  difference := num1 - num2;
  product := num1 * num2;
  quotient := num1 / num2;

  { Displaying the results }
  WriteLn('First number: ', num1:0:2);
  WriteLn('Second number: ', num2:0:2);
  WriteLn('Sum: ', sum:0:2);
  WriteLn('Difference: ', difference:0:2);
  WriteLn('Product: ', product:0:2);
  WriteLn('Quotient: ', quotient:0:2);
end.