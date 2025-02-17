# Sistema de Gestão de Patrimônio com Django

Sistema para gerenciamento de bens em uma empresa, permitindo cadastro, transferência entre setores, agendamento de manutenções e monitoramento do status de cada bem.

---

## Funcionalidades Principais

1. **Cadastro de Bens**
   - Cada bem é cadastrado com uma identificação única no formato RFID (XX:XX:XX:XX).
   - Informações como nome, categoria, departamento, valor e status de manutenção são registradas.

2. **Transferência de Bens**
   - Os bens podem ser transferidos entre diferentes departamentos.
   - Todas as transferências são registradas, criando um histórico completo.

3. **Agendamento de Manutenções**
   - É possível agendar manutenções, definindo data e descrição.
   - O status da manutenção (Agendada, Em Andamento, Concluída) é atualizado automaticamente, refletindo no status do bem.

4. **Monitoramento de Status**
   - O sistema exibe o status de cada bem (OK, Em Manutenção, Próximo da Revisão) e as manutenções agendadas.
   - Quando uma manutenção é agendada ou iniciada, o status do bem é automaticamente alterado para "Em Manutenção".

5. **Interface Administrativa Segura**
   - A interface administrativa foi configurada para limitar as permissões dos administradores, evitando fraudes ou alterações indevidas.
   - Por exemplo, nas manutenções, os administradores só podem alterar o status, sem editar outros campos.

---

## Como Funciona

### Tela Inicial
A tela inicial (`show.html`) exibe diferentes tabelas dependendo do contexto:
- **Bens:** Lista todos os bens cadastrados.
- **Movimentações:** Exibe o histórico de transferências.
- **Manutenções:** Mostra as manutenções agendadas.

### Permissões Administrativas
A interface administrativa foi personalizada para garantir a segurança:
- **Manutenções:**
  - Administradores só podem alterar o status das manutenções.
  - Campos como bem, data agendada e descrição são bloqueados para edição.
- **Movimentações:**
  - Administradores só podem visualizar e excluir movimentações.
  - A adição e edição de movimentações são desabilitadas.