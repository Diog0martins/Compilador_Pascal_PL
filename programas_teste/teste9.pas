program AverageCalculator;

var
  num, count: Integer;
  sum, average1, average2, average3: Real;
  numeros: array[1..5] of string;

begin 

  if count > 0 then
  begin
    average := sum / count;
    average2 := sum2 / count2;
    writeln('The average of the entered numbers is: ', average);
  end;
  else
    average := sum / count;
    writeln('No numbers were entered.');

end.