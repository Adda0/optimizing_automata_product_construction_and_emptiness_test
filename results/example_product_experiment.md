# Example product experiment results
| Automaton A | Automaton B | Checked | Processed | Satisfiable | Unsatisfiable | Skipped |Handle and Loop A | Handle and Loop B | Product Optimized | Product Basic | Product Final States | Spared state space |
| - | - | - | - | - | - | - | - | - | - | - | - | - |
| 6 | 4 | 6 | 5 | 3 | 2 | 1 | 8 | 6 | 4 | 9 | 1 | 5 |

We have started with automata of sizes 6 and 4 states. Our algorithm checked 6 states (suggested to test 6 states), from which we have executed satisfiabilty check for 5 of them (processed). One state could be skipped using our skip satisfiable product states optimization. From the tested 5 states, 3 were satisfiable (fulfilled the length constrains) and 2 of them could be omitted because of unsatistiable result of the satisfiability check. The final product had one accept state and complete generated state space was 4 product states for our optimized algorithm in comparison to 9 product states in the basic product construction algorithm. In total, we have spare 5 product states, which don't need to be in the final product, because there is no accepting run from these states in the product automaton.
