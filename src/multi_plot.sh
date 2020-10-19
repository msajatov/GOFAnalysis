mkdir -p "/eos/user/m/msajatov/wormhole/pvalue_plots/err/mc"

for CH in et mt tt; do
    for TEST in saturated KS AD; do
        python gof.py -c $CH -i output -m plot --test $TEST -err cc cc1 cc2
    done
done

mv /eos/user/m/msajatov/wormhole/pvalue_plots/*.pdf "/eos/user/m/msajatov/wormhole/pvalue_plots/err/mc"
mv /eos/user/m/msajatov/wormhole/pvalue_plots/*.png "/eos/user/m/msajatov/wormhole/pvalue_plots/err/mc"

mkdir -p "/eos/user/m/msajatov/wormhole/pvalue_plots/err/emb"

for CH in et mt tt; do
    for TEST in saturated KS AD; do
        python gof.py -c $CH -i output -m plot --test $TEST -err ccemb ccemb1 ccemb2   
    done
done

mv /eos/user/m/msajatov/wormhole/pvalue_plots/*.pdf "/eos/user/m/msajatov/wormhole/pvalue_plots/err/emb"
mv /eos/user/m/msajatov/wormhole/pvalue_plots/*.png "/eos/user/m/msajatov/wormhole/pvalue_plots/err/emb"