mkdir -p "/eos/user/m/msajatov/wormhole/pvalue_plots/nn_err/comp"

for CH in et mt tt; do
    for TEST in saturated KS AD; do
        python gof.py -c $CH -i output -m plot --test $TEST -err snn30 snn32 snn47 snn48 snn51 snn13 snn28 snn6 snn8 snn15 snn14 snn49
    done
done

mv /eos/user/m/msajatov/wormhole/pvalue_plots/*.pdf "/eos/user/m/msajatov/wormhole/pvalue_plots/nn_err/comp"
mv /eos/user/m/msajatov/wormhole/pvalue_plots/*.png "/eos/user/m/msajatov/wormhole/pvalue_plots/nn_err/comp"