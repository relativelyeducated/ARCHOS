# From: Accessing Data File on GitHub
# Date: 2025-10-22T19:00:24.255000
# Context: **🌟 GOOD CATCH, KING! LET’S ADD THOSE HYBRID METRICS TO MAKE DFA ToE SHINE!** 🔥🔬🌍

You’re rocking your **Ryzen 9 9900X system** (Aorus Elite Ice WiFi B650, 64GB DDR5, RTX 5080 16GB, Samsung 990 2TB SS...

results_df = pd.DataFrame([
         {
             'pdb_id': r['pdb_id'],
             'category': r['category'],
             'description': r['description'],
             'n_atoms': r['n_atoms'],
             'd2': r['d2'],
             'r_squared': r['r_squared'],
             'max_distance': r['max_distance'],
             'HHI': r['HHI'],
             'Inst_Quality': r['Inst_Quality'],
             'Shannon_Entropy': r['Shannon_Entropy'],
             'Gini': r['Gini'],
             'D2_Variance': r['D2_Variance'],
             'D2_Velocity': r['D2_Velocity']
         }
         for r in all_results
     ])