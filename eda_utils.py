import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import streamlit as st
from typing import Optional

# Set styling
sns.set_palette("husl")
plt.style.use('seaborn-v0_8-darkgrid')


def load_data(uploaded_file) -> Optional[pd.DataFrame]:
    """
    Load CSV data from uploaded file with error handling.
    
    Args:
        uploaded_file: Streamlit uploaded file object
        
    Returns:
        DataFrame or None if loading fails
    """
    try:
        if uploaded_file is not None:
            # Try reading with different parameters
            try:
                df = pd.read_csv(uploaded_file)
            except:
                uploaded_file.seek(0)
                df = pd.read_csv(uploaded_file, skiprows=1)
            
            # Basic validation
            if df.empty:
                st.error("The uploaded file is empty")
                return None
            
            # Remove unnamed columns
            df = df.loc[:, ~df.columns.str.contains('^Unnamed')]
            
            return df
    except Exception as e:
        st.error(f"Error loading file: {str(e)}")
        return None


def show_data_preview(df: pd.DataFrame, rows: int = 10) -> None:
    """
    Display preview of the dataset.
    
    Args:
        df: Input DataFrame
        rows: Number of rows to display
    """
    try:
        st.markdown(f"### 📋 Data Preview (First {rows} rows)")
        st.dataframe(
            df.head(rows),
            use_container_width=True,
            height=400
        )
    except Exception as e:
        st.error(f"Error displaying data preview: {str(e)}")


def show_summary_stats(df: pd.DataFrame) -> None:
    """
    Display comprehensive summary statistics.
    
    Args:
        df: Input DataFrame
    """
    try:
        st.markdown("### 📊 Summary Statistics")
        
        numeric_df = df.select_dtypes(include=['number'])
        
        if numeric_df.empty:
            st.warning("No numeric columns found in the dataset")
            return
        
        # Calculate statistics
        desc = numeric_df.describe().T
        desc['median'] = numeric_df.median()
        desc['variance'] = numeric_df.var()
        desc['skewness'] = numeric_df.skew()
        desc['kurtosis'] = numeric_df.kurtosis()
        
        # Reorder columns for better readability
        column_order = ['count', 'mean', 'median', 'std', 'variance', 
                       'min', '25%', '50%', '75%', 'max', 'skewness', 'kurtosis']
        desc = desc[[col for col in column_order if col in desc.columns]]
        
        # Format the dataframe
        st.dataframe(
            desc.style.format("{:.2f}").background_gradient(cmap='coolwarm', axis=1),
            use_container_width=True
        )
        
        # Additional insights
        with st.expander("📈 Statistical Insights"):
            for col in numeric_df.columns:
                skew = numeric_df[col].skew()
                if abs(skew) > 1:
                    skew_type = "highly skewed"
                elif abs(skew) > 0.5:
                    skew_type = "moderately skewed"
                else:
                    skew_type = "approximately symmetric"
                
                st.write(f"**{col}**: {skew_type} (skewness: {skew:.2f})")
                
    except Exception as e:
        st.error(f"Error calculating summary statistics: {str(e)}")


def show_missing_values(df: pd.DataFrame) -> None:
    """
    Display detailed missing values analysis.
    
    Args:
        df: Input DataFrame
    """
    try:
        st.markdown("### 🔍 Missing Values Analysis")
        
        missing = df.isnull().sum()
        missing_pct = (missing / len(df)) * 100
        
        missing_df = pd.DataFrame({
            'Column': missing.index,
            'Missing Count': missing.values,
            'Percentage': missing_pct.values
        })
        
        missing_df = missing_df[missing_df['Missing Count'] > 0].sort_values(
            'Missing Count', ascending=False
        )
        
        if missing_df.empty:
            st.success("✅ No missing values detected in the dataset!")
        else:
            st.warning(f"⚠️ Found missing values in {len(missing_df)} columns")
            
            # Display table
            st.dataframe(
                missing_df.style.format({
                    'Missing Count': '{:.0f}',
                    'Percentage': '{:.2f}%'
                }).background_gradient(cmap='Reds', subset=['Percentage']),
                use_container_width=True,
                hide_index=True
            )
            
            # Visualization
            if len(missing_df) > 0:
                fig, ax = plt.subplots(figsize=(10, max(4, len(missing_df) * 0.3)))
                ax.barh(missing_df['Column'], missing_df['Percentage'], color='#E74C3C')
                ax.set_xlabel('Missing Percentage (%)', fontsize=12)
                ax.set_ylabel('Column', fontsize=12)
                ax.set_title('Missing Values by Column', fontsize=14, fontweight='bold')
                plt.tight_layout()
                st.pyplot(fig)
                plt.close()
                
    except Exception as e:
        st.error(f"Error analyzing missing values: {str(e)}")


def show_data_types(df: pd.DataFrame) -> None:
    """
    Display data types information.
    
    Args:
        df: Input DataFrame
    """
    try:
        st.markdown("### 📋 Data Types")
        
        dtype_df = pd.DataFrame({
            'Column': df.columns,
            'Data Type': df.dtypes.astype(str),
            'Non-Null Count': df.count(),
            'Null Count': df.isnull().sum()
        })
        
        st.dataframe(
            dtype_df,
            use_container_width=True,
            hide_index=True
        )
        
        # Summary
        col1, col2, col3 = st.columns(3)
        with col1:
            numeric_count = len(df.select_dtypes(include=['number']).columns)
            st.metric("Numeric Columns", numeric_count)
        with col2:
            categorical_count = len(df.select_dtypes(include=['object']).columns)
            st.metric("Categorical Columns", categorical_count)
        with col3:
            datetime_count = len(df.select_dtypes(include=['datetime']).columns)
            st.metric("Datetime Columns", datetime_count)
            
    except Exception as e:
        st.error(f"Error displaying data types: {str(e)}")


def show_correlations(df: pd.DataFrame) -> None:
    """
    Display correlation matrix heatmap with enhanced styling.
    
    Args:
        df: Input DataFrame
    """
    try:
        st.markdown("### 🔥 Correlation Matrix")
        
        numeric_df = df.select_dtypes(include=['number'])
        
        if numeric_df.shape[1] < 2:
            st.warning("Need at least 2 numeric columns to compute correlations")
            return
        
        corr = numeric_df.corr()
        
        # Create figure with better size
        fig, ax = plt.subplots(figsize=(12, 10))
        
        # Create mask for upper triangle
        mask = np.triu(np.ones_like(corr, dtype=bool))
        
        # Enhanced heatmap
        sns.heatmap(
            corr,
            mask=mask,
            annot=True,
            fmt='.2f',
            cmap='coolwarm',
            center=0,
            square=True,
            linewidths=1,
            cbar_kws={"shrink": 0.8},
            ax=ax,
            vmin=-1,
            vmax=1
        )
        
        ax.set_title('Correlation Heatmap', fontsize=16, fontweight='bold', pad=20)
        plt.tight_layout()
        st.pyplot(fig)
        plt.close()
        
        # Show strong correlations
        with st.expander("🔍 Strong Correlations (|r| > 0.7)"):
            strong_corr = []
            for i in range(len(corr.columns)):
                for j in range(i+1, len(corr.columns)):
                    if abs(corr.iloc[i, j]) > 0.7:
                        strong_corr.append({
                            'Variable 1': corr.columns[i],
                            'Variable 2': corr.columns[j],
                            'Correlation': corr.iloc[i, j]
                        })
            
            if strong_corr:
                strong_df = pd.DataFrame(strong_corr).sort_values(
                    'Correlation', key=abs, ascending=False
                )
                st.dataframe(
                    strong_df.style.format({'Correlation': '{:.3f}'}),
                    use_container_width=True,
                    hide_index=True
                )
            else:
                st.info("No strong correlations found (threshold: |r| > 0.7)")
                
    except Exception as e:
        st.error(f"Error calculating correlations: {str(e)}")


def show_histogram(df: pd.DataFrame, column: str, bins: int = 30) -> None:
    """
    Plot enhanced histogram for a selected column.
    
    Args:
        df: Input DataFrame
        column: Column name to plot
        bins: Number of bins for histogram
    """
    try:
        if column not in df.columns:
            st.error(f"Column '{column}' not found in dataset")
            return
        
        st.markdown(f"#### 📊 Distribution of {column}")
        
        fig, ax = plt.subplots(figsize=(10, 6))
        
        # Plot histogram with KDE
        data = df[column].dropna()
        
        ax.hist(data, bins=bins, alpha=0.7, color='#4A90E2', edgecolor='black', density=True)
        
        # Add KDE line
        if len(data) > 1:
            from scipy import stats
            kde = stats.gaussian_kde(data)
            x_range = np.linspace(data.min(), data.max(), 100)
            ax.plot(x_range, kde(x_range), 'r-', linewidth=2, label='KDE')
        
        ax.set_xlabel(column, fontsize=12, fontweight='bold')
        ax.set_ylabel('Density', fontsize=12, fontweight='bold')
        ax.set_title(f'Distribution of {column}', fontsize=14, fontweight='bold')
        ax.legend()
        ax.grid(True, alpha=0.3)
        
        plt.tight_layout()
        st.pyplot(fig)
        plt.close()
        
        # Show statistics
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Mean", f"{data.mean():.2f}")
        with col2:
            st.metric("Median", f"{data.median():.2f}")
        with col3:
            st.metric("Std Dev", f"{data.std():.2f}")
        with col4:
            st.metric("Count", f"{len(data)}")
            
    except Exception as e:
        st.error(f"Error creating histogram: {str(e)}")


def show_boxplot(df: pd.DataFrame, x_col: str, y_col: str) -> None:
    """
    Plot enhanced boxplot.
    
    Args:
        df: Input DataFrame
        x_col: Column for x-axis (categories)
        y_col: Column for y-axis (values)
    """
    try:
        if x_col not in df.columns or y_col not in df.columns:
            st.error("Selected columns not found in dataset")
            return
        
        st.markdown(f"#### 📦 Box Plot: {y_col} by {x_col}")
        
        # Limit categories if too many
        unique_vals = df[x_col].nunique()
        if unique_vals > 20:
            st.warning(f"Too many categories ({unique_vals}). Showing top 20 by frequency.")
            top_categories = df[x_col].value_counts().head(20).index
            plot_df = df[df[x_col].isin(top_categories)]
        else:
            plot_df = df
        
        fig, ax = plt.subplots(figsize=(12, 6))
        
        sns.boxplot(
            data=plot_df,
            x=x_col,
            y=y_col,
            ax=ax,
            palette='Set2'
        )
        
        ax.set_xlabel(x_col, fontsize=12, fontweight='bold')
        ax.set_ylabel(y_col, fontsize=12, fontweight='bold')
        ax.set_title(f'{y_col} by {x_col}', fontsize=14, fontweight='bold')
        
        # Rotate labels if needed
        if unique_vals > 5:
            plt.xticks(rotation=45, ha='right')
        
        ax.grid(True, alpha=0.3, axis='y')
        plt.tight_layout()
        st.pyplot(fig)
        plt.close()
        
    except Exception as e:
        st.error(f"Error creating boxplot: {str(e)}")


def show_scatter(df: pd.DataFrame, x_col: str, y_col: str) -> None:
    """
    Plot enhanced scatter plot.
    
    Args:
        df: Input DataFrame
        x_col: Column for x-axis
        y_col: Column for y-axis
    """
    try:
        if x_col not in df.columns or y_col not in df.columns:
            st.error("Selected columns not found in dataset")
            return
        
        st.markdown(f"#### 🔵 Scatter Plot: {x_col} vs {y_col}")
        
        fig, ax = plt.subplots(figsize=(10, 6))
        
        # Create scatter plot
        ax.scatter(
            df[x_col],
            df[y_col],
            alpha=0.6,
            c='#4A90E2',
            edgecolors='black',
            linewidth=0.5,
            s=50
        )
        
        # Add regression line if both are numeric
        if df[x_col].dtype in ['int64', 'float64'] and df[y_col].dtype in ['int64', 'float64']:
            z = np.polyfit(df[x_col].dropna(), df[y_col].dropna(), 1)
            p = np.poly1d(z)
            ax.plot(
                df[x_col],
                p(df[x_col]),
                "r--",
                linewidth=2,
                alpha=0.8,
                label=f'Trend: y={z[0]:.2f}x+{z[1]:.2f}'
            )
            ax.legend()
        
        ax.set_xlabel(x_col, fontsize=12, fontweight='bold')
        ax.set_ylabel(y_col, fontsize=12, fontweight='bold')
        ax.set_title(f'{x_col} vs {y_col}', fontsize=14, fontweight='bold')
        ax.grid(True, alpha=0.3)
        
        plt.tight_layout()
        st.pyplot(fig)
        plt.close()
        
        # Calculate and display correlation
        if df[x_col].dtype in ['int64', 'float64'] and df[y_col].dtype in ['int64', 'float64']:
            corr = df[[x_col, y_col]].corr().iloc[0, 1]
            st.info(f"📊 Pearson Correlation: {corr:.3f}")
            
    except Exception as e:
        st.error(f"Error creating scatter plot: {str(e)}")


def show_distribution(df: pd.DataFrame, column: str) -> None:
    """
    Show distribution plot with multiple views.
    
    Args:
        df: Input DataFrame
        column: Column name to analyze
    """
    try:
        if column not in df.columns:
            st.error(f"Column '{column}' not found in dataset")
            return
        
        st.markdown(f"#### 📈 Distribution Analysis: {column}")
        
        data = df[column].dropna()
        
        fig, axes = plt.subplots(1, 2, figsize=(14, 5))
        
        # Histogram with KDE
        axes[0].hist(data, bins=30, alpha=0.7, color='#4A90E2', edgecolor='black', density=True)
        if len(data) > 1:
            from scipy import stats
            kde = stats.gaussian_kde(data)
            x_range = np.linspace(data.min(), data.max(), 100)
            axes[0].plot(x_range, kde(x_range), 'r-', linewidth=2)
        axes[0].set_title('Histogram with KDE', fontweight='bold')
        axes[0].set_xlabel(column)
        axes[0].set_ylabel('Density')
        axes[0].grid(True, alpha=0.3)
        
        # Box plot
        axes[1].boxplot(data, vert=True)
        axes[1].set_title('Box Plot', fontweight='bold')
        axes[1].set_ylabel(column)
        axes[1].grid(True, alpha=0.3)
        
        plt.tight_layout()
        st.pyplot(fig)
        plt.close()
        
    except Exception as e:
        st.error(f"Error creating distribution plot: {str(e)}")