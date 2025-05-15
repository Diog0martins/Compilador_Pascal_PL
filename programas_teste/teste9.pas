program SimpleAssignment;
var
  num, i: integer;
  test: string;
begin
  num := 42;
  i := 30;
  while num < 50 do 
  begin
    num := num + 2;
    i := i div 2;
  end;
end.