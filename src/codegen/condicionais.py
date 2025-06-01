from loops_table import counter

def gerar_condicionais(condicao,true_body,false_body):

    # Incrementar o contador de ifs
    counter.inc_if()

    # Gerar as labels necessárias
    false_label = f'ELSE{counter.get_if()}'
    end_if = f'ENDIF{counter.get_if()}'
    check_cond = f'JZ {false_label}'
    end_true_body = f'JUMP {end_if}'

    # Retornar o código para a condicional
    return "\n".join([condicao,
                      check_cond,
                      true_body,
                      end_true_body,
                      false_label+':',
                      false_body,
                      end_if+ ':'])