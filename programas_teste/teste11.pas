program ProgramaSoma;

function SomaDois(a,b,c: Integer): Integer;
begin
  SomaDois := a * b * c;
end;

var
  resultado, num: Integer;

begin
  num := 5;
  resultado := SomaDois(2,3,num);
end.
