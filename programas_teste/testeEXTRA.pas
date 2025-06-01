program VerificaPalindromo;

var
  palavra: string;
  i, tamanho: integer;
  ehPalindromo: boolean;

function CaracterIguais(a, b: char): boolean;
begin
  CaracterIguais := a = b;
end;

begin
  writeln('Introduza uma palavra:');
  readln(palavra);
  tamanho := length(palavra);
  ehPalindromo := true;

  for i := 1 to tamanho div 2 do
  begin
    if not CaracterIguais(palavra[i], palavra[tamanho - i + 1]) then
      ehPalindromo := false;
  end;

  if ehPalindromo then
    writeln('É palíndromo!')
  else
    writeln('Não é palíndromo.');
end.