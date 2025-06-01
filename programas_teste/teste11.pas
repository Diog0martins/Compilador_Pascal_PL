program ProgramaSoma;

function SomaDois(a: Integer): Integer;
begin
  a := 2;
  SomaDois := a * 2;
end;

var
  resultado, num: Integer;

begin
  resultado := SomaDois(2);
end.
