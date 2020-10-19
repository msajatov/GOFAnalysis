mkdir -p "/eos/user/m/msajatov/wormhole/pvalue_plots/sensitivity"

for CH in et mt tt; do
    for TEST in saturated KS AD; do
        python gof.py -c $CH -i output -m plot --test $TEST -bg snn30 snn32 snn47 snn48 snn51 snn31 snn15 snn14 snn49 snn52 -err xx w tt -dummy NN       
    done
done

mv /eos/user/m/msajatov/wormhole/pvalue_plots/*.pdf "/eos/user/m/msajatov/wormhole/pvalue_plots/sensitivity"
mv /eos/user/m/msajatov/wormhole/pvalue_plots/*.png "/eos/user/m/msajatov/wormhole/pvalue_plots/sensitivity"
