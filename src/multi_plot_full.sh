mkdir -p "/eos/user/m/msajatov/wormhole/pvalue_plots/err/mc"

for CH in et mt tt; do
    for TEST in saturated KS AD; do
        python gof.py -c $CH -i output -m plot --test $TEST -err cc cc1 cc2 -bg snn30 snn32 snn48 snn47 snn31 snn15 snn14 snn49 -dummy NN
    done
done

mv /eos/user/m/msajatov/wormhole/pvalue_plots/*.pdf "/eos/user/m/msajatov/wormhole/pvalue_plots/err/mc"
mv /eos/user/m/msajatov/wormhole/pvalue_plots/*.png "/eos/user/m/msajatov/wormhole/pvalue_plots/err/mc"

mkdir -p "/eos/user/m/msajatov/wormhole/pvalue_plots/err/emb"

for CH in et mt tt; do
    for TEST in saturated KS AD; do
        python gof.py -c $CH -i output -m plot --test $TEST -err ccemb ccemb1 ccemb2 -bg snn30 snn32 snn48 snn47 snn31 snn15 snn14 snn49 -dummy NN
    done
done

mv /eos/user/m/msajatov/wormhole/pvalue_plots/*.pdf "/eos/user/m/msajatov/wormhole/pvalue_plots/err/emb"
mv /eos/user/m/msajatov/wormhole/pvalue_plots/*.png "/eos/user/m/msajatov/wormhole/pvalue_plots/err/emb"