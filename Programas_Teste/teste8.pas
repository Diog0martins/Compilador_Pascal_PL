program AverageCalculator;

uses crt;

var
  num, count: Integer;
  sum, average: Real;

begin
  clrscr;
  sum := 0;
  count := 0;

  writeln('Enter numbers to calculate the average (enter 0 to stop):');

  repeat
    write('Enter a number: ');
    readln(num);

    if num <> 0 then
    begin
      sum := sum + num;
      count := count + 1;
    end;

  until num = 0;

  if count > 0 then
  begin
    average := sum / count;
    writeln('The average of the entered numbers is: ', average:0:2);
  end
  else
    writeln('No numbers were entered.');

  readln;
end.
