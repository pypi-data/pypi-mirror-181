import itertools
import pandas as pd
import matplotlib.pyplot as plt
import scipy.stats as stats

# optional packages
try:
    import pingouin as pg
except:
    pass

try:
    from statsmodels.stats.multitest import fdrcorrection
except:
    pass

try:
    import seaborn as sns
except:
    pass

def tukey_outliers(df, var, distance=3, mode="print"):
    """
    Function to identify outliers using the Tukey method.
    
    Parameters
    ----------
    df : pandas dataframe
        Dataframe containing the variable of interest.
    var : str
        Name of the variable to identify outliers in.
    distance : int, optional
        Distance from the median to consider an outlier. The default is 3.
    mode : str, optional
        Mode to return the outliers. The default is "print".
    
    Returns
    -------
    list
        List of outliers. Only if mode is "return". Otherwise, None.
    """

    q1 = df[var].quantile(0.25)
    q3 = df[var].quantile(0.75)

    iqr = q3-q1
    outlier_lower = q1 - (iqr*distance)
    outlier_upper = q3 + (iqr*distance)
    mask_outlier = (df[var] < outlier_lower) | (df[var] > outlier_upper)
    if mode == "print":
        print(
            f"25th Percentile (Q1): {q1:.2f}\n75th Percentile (Q3): {q3:.2f}\nIQR: {iqr:.2f}")
        print(
            f"Will count cases as outlier with values less than {outlier_lower:.2f} or more than {outlier_upper:.2f}.")
        if df[mask_outlier].shape[0] == 0:
            print("With these criteria there are no outlier in the data")
        else:
            print("Showing outliers")
            print(df[mask_outlier][var].to_string())
    elif mode == "return":
        return list(df[mask_outlier][var].index.values)
    else:
        print("Mode must be 'print' or 'return'")


def qqs_over_groups_and_vars(df, group_label, vars_li, size=(15, 15)):
    """
    Function to plot QQ subplots for each variable in a list of variables, over groups in a categorical variable.

    Parameters
    ----------
    df : pandas dataframe
        Dataframe containing the variables of interest.
    group_label : str
        Name of the categorical variable to group the data.
    vars_li : list
        List of variables to plot.
    size : tuple, optional
        Size of the plot to draw subplots in. The default is (15, 15).

    Returns
    -------
    None. 
    """
    groups_li = df[group_label].unique()
    fig, axes = plt.subplots(len(groups_li), len(vars_li), figsize=size)
    fig.tight_layout(pad=5.0)
    plt.grid(False)

    x = 0
    y = 0
    for group, var in itertools.product(groups_li, vars_li):
        stats.probplot(df[df[group_label] == group][var],
                       dist="norm", plot=axes[y, x])
        axes[y, x].set_title(group + " - " + var)
        if x < (len(vars_li)-1):
            x += 1
        else:
            x = 0
            y += 1


def check_homoscedacity(y_var, group_var, df):
    """
    Function to check for homoscedacity using heuristics recommended by Blanca et al. (2018).
    
    Parameters
    ----------
    y_var : str
        Name of the variable to check for homoscedacity.
    group_var : str
        Name of the categorical variable to group the data.
    df : pandas dataframe
        Dataframe containing the variables of interest.

    Returns
    -------
    None. 
    """

    var_ser = pd.Series(index=df[group_var].unique(), dtype=float)

    for group in df[group_var].unique():
        var_ser[group] = df[df[group_var] == group][y_var].var()

    min_var = (var_ser.idxmin(), var_ser.min())
    max_var = (var_ser.idxmax(), var_ser.max())
    var_ratio = max_var[1]/min_var[1]
    print(f"Smallest variance for {min_var[0]}: {min_var[1]:.2f}")
    print(f"Largest variance for {max_var[0]}: {max_var[1]:.2f}")
    print(f"Variance ratio: {var_ratio:.2f}")

    if var_ratio <= 1.5:
        print("Variance ratio is <= 1.5, F-test will be robust.")
        return
    else:
        print("Variance ratio is > 1.5. Now doing additional checks to see if F-test is robust.")

    # Create dataframe with variance and group sizes
    var_n_df = var_ser.to_frame(name="var")
    var_n_df["n"] = df.value_counts(subset=group_var)
    # get correlation between correlation and variance
    corr_var_n = var_n_df[["var", "n"]].corr().iloc[1, 0]

    if (corr_var_n >= 0) and (corr_var_n <= 0.5):
        print(
            f"Correlation between sample size and variance (pairing) is {corr_var_n:.2f}."
            f" That is between 0 and .5. F-test should be robust")
        return
    else:
        print(
            f"Correlation between sample size and variance (pairing) is {corr_var_n:.2f}.")

    # Compute coefficient of sample size variation
    coeff_n = var_n_df["var"].std()/var_n_df["var"].mean()
    if (corr_var_n > 0.5) and (coeff_n > .33) and (var_ratio > 2):
        print(f"Pairing is {corr_var_n:.2f}, so larger than .5."
              f" The coefficient of sample size variation is {coeff_n:.2f}, larger than .33."
              f" The variance ratio is {var_ratio:.2f}, larger than 2."
              f" F-test is too conserative (hurting power)")
    elif (corr_var_n < 0) and (corr_var_n >= -0.5) and (coeff_n > .16) and (var_ratio > 2):
        print(f"Pairing is {corr_var_n:.2f}, so smaller than 0 and larger than or equal to -.5."
              f" The coefficient of sample size variation is {coeff_n:.2f}, larger than .16."
              f" The variance ratio is {var_ratio:.2f}, larger than 2."
              f" F-test is too liberal (real alpha might be as high as .1 if variance ratio is 9 or smaller).")
    elif (corr_var_n < -0.5):
        print(f"Pairing is {corr_var_n:.2f}, so smaller than -.5."
              f" F-test is too liberal (real alpha might be as high as .2 if variance ratio is 9 or smaller).")
    else:
        print(
            f"Pairing is {corr_var_n:.2f}, coefficient of sample size variation is {coeff_n:.2f},"
            f" and the variance ratio is {var_ratio:.2f}."
            f" This specific combination should have robust F-test, but look into the paper",
            f" ('Effect of variance ratio on ANOVA robustness: Might 1.5 be the limit?', Blanca et al., 2018)",
            f" to be sure."
            )

def compare_var_mult_groups(df, dv, group_var, alpha=0.05, adj_p = True, print_results = True, return_results = True, method = "levene"):
    """
    Compare the variance of a variable between multiple groups. Requires the pingouin package.

    Will conduct a Levene or Bartlett test as an omnibus test first.
    This omnibus test will be followed up by post hoc tests.
    For the post-hoc tests, each group will be compared to the rest of the groups. p-values will be adjusted for multiple comparisons using FDR correction.

    Parameters
    ----------
    df : pandas DataFrame
        The DataFrame containing the data.
    dv : str
        The name of the variable to compare the variance of.
    group_var : str
        The name of the variable containing the groups.
    alpha : float
        The significance level to use for the tests. Default is 0.05.
    adj_p : bool
        Whether to adjust the p-values for multiple comparisons. Default is True. This will use FDR correction. This option requires the statsmodels package.
    print_results : bool
        Whether to print a report of the results. Default is True.
    return_results : bool
        Whether to return the results. Default is True.
    method : str
        The method to use for the omnibus test. Default is "levene". Can also be "bartlett".

    Returns
    -------
    omnibus : pandas DataFrame
        Only returned when return_results = True. A pandas DataFrame containing the results of the omnibus test. 
    posthoc : dict
        Only returned when return_results = True. A dictionary containing the results of the post hoc tests. The keys are the group names. The values are pandas DataFrames containing the results of the post hoc tests for that group.
    """

    # Omnibus test
    omnibus = pg.homoscedasticity(
        df, dv=dv, group=group_var, method=method, alpha=alpha
        )

    # Post hoc tests
    # compare each preset against rest
    # store results in dict with preset as key, and a pandas df as value
    # the df contains the columns 'W', 'pval', 'equal_var'
    posthoc = {}

    groups = df[group_var].unique()
        
    for group in groups:
        data_group = df[
            df[group_var] == group
            ][dv].to_numpy()
        data_rest = df[
            df[group_var] != group
            ][dv].to_numpy()
        posthoc[group] = pg.homoscedasticity(
            [data_group, data_rest], method=method, alpha=alpha
            )

    # collect a p-values from the posthoc tests in a list
    ps = []
    for group in posthoc:
        ps.append(posthoc[group].iloc[0, 1])
    # correct for multiple comparisons with FDR
    if adj_p:
        adj_ps = fdrcorrection(ps, alpha=0.1)[1]

    i = 0
    # Go through posthoc dict
    # For each category, add SD and adj. p (if applicable) to the df 
    for group in posthoc:
        posthoc[group].loc[
            method, "sd"
            ] = df[df[group_var] == group][dv].std()
        if adj_p:
            posthoc[group].loc[method, "adj_p"] = adj_ps[i]
        i += 1

    # Print results
    if print_results:
        print(f"Omnibus test:\n{omnibus.round(4).to_string()}\n")

        # Print post hoc results
        if omnibus.iloc[0, 2] == False:
            print(
                f"Variances are not equal, doing posthoc tests:"
                f"\nAverage SD: {df[dv].std():.4f}"
                )
            if adj_p:
                print(f"\nPresets with adjusted p-vals < {alpha:.2f} displayed below:")
            else:
                print(f"\nPresets with p-vals < {alpha:.2f} displayed below:")

            any_sig = False
            for group in posthoc:
                if adj_p:
                    if posthoc[group].iloc[0, 4] < alpha:
                        print(f"\n{group}:")
                        print(posthoc[group].round(4).to_string())
                        any_sig = True
                else:
                    if posthoc[group].iloc[0, 1] < alpha:
                        print(f"\n{group}:")
                        print(posthoc[group].round(4).to_string())
                        any_sig = True

            if not any_sig:
                print("No significant differences for any of the groups (vs. rest).")

    if return_results:
        return omnibus, posthoc

def hist_over_groups(df, var, var_name, group_label, groups,
                     bins_n=10, xlim=(-3, 3), size=(15, 15),
                     plot_avg=True, save_plot=False,
                     ):
    """
    Plot histograms for a selection of groups.

    Parameters
    ----------
    df : pandas DataFrame
        The DataFrame containing the data.
    var : str
        The name of the variable to plot.
    var_name : str
        The label for the variable to plot. This will be used as the title of the plot.
    group_label : str
        The name of the variable containing the groups.
    groups : list
        The groups to plot.
    bins_n : int, optional
        The number of bins to use for the histograms. Default is 10.
    xlim : tuple, optional
        The x-axis limits. Default is (-3, 3).
    size : tuple, optional
        The size of the plot. Default is (15, 15).
    plot_avg : bool, optional
        Whether to include a plot of the grand mean over all groups. Default is True.
    
    Returns
    -------
    None
    """

    n_plots = len(groups)+1 if plot_avg else len(groups)
    fig, axes = plt.subplots(1, n_plots, figsize=size)
    fig.tight_layout(pad=5.0)

    x = 0

    if plot_avg:
        df[var].plot.hist(ax=axes[x], bins=bins_n)
        df[var].plot.kde(ax=axes[x], secondary_y=True)
        axes[x].set_xlim(xlim)
        axes[x].set_title(f"{var_name} - Average")
        axes[x].grid(False)
        x += 1

    for group in groups:
        df_group = df[df[group_label] == group]
        df_group[var].plot.hist(ax=axes[x], bins=bins_n)
        df_group[var].plot.kde(ax=axes[x], secondary_y=True)
        axes[x].set_xlim(xlim)
        axes[x].set_title(f"{var_name} - {group}")
        axes[x].grid(False)
        x += 1

    if save_plot:
        fig.savefig(save_plot, bbox_inches="tight")


def box_over_groups(df, var, var_name, group_label, groups,
                    ylim=(-3, 3), size=(15, 15),
                    plot_avg=True, save_plot=False):
    """
    Plot boxplots for a selection of groups. Requires seaborn.

    Parameters
    ----------
    df : pandas DataFrame
        The DataFrame containing the data.
    var : str
        The name of the variable to plot.
    var_name : str
        The label for the variable to plot. This will be used as the title of the plot.
    group_label : str
        The name of the variable containing the groups.
    groups : list
        The groups to plot.
    ylim : tuple, optional
        The y-axis limits. Default is (-3, 3).
    size : tuple, optional
        The size of the plot. Default is (15, 15).
    plot_avg : bool, optional
        Whether to include a plot of the grand mean over all groups. Default is True.
    save_plot : bool, optional
        Whether to save the plot. Default is False.
    
    Returns
    -------
    None
    """

    n_plots = len(groups)+1 if plot_avg else len(groups)
    fig, axes = plt.subplots(1, n_plots, figsize=size)
    fig.tight_layout(pad=5.0)

    x = 0

    if plot_avg:
        sns.boxplot(y=df[var], ax=axes[x])
        axes[x].set_ylim(ylim)
        axes[x].set_title(f"{var_name} - Average")
        axes[x].grid(False)
        x += 1

    for group in groups:
        df_group = df[df[group_label] == group]
        sns.boxplot(y=df_group[var], ax=axes[x])
        axes[x].set_ylim(ylim)
        axes[x].set_title(f"{var_name} - {group}")
        axes[x].grid(False)
        x += 1

    if save_plot:
        fig.savefig(save_plot, bbox_inches="tight")
