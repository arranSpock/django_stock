from django.shortcuts import render, redirect
from .models import Stock
from django.contrib import messages
from .forms import StockForm

def home(request):
    
    import requests
    import json

    if request.method =='POST':
        ticker = request.POST['ticker']
        api_request = requests.get("https://financialmodelingprep.com/stable/quote?symbol="+ticker+"&apikey=b5249712421ee83869be287077e59a29")

        try:
            api = json.loads(api_request.content)
            if not api:
                api='No data found for this ticker.'
        except Exception as e:
            api = 'No data found for this ticker.'
        return render(request,'home.html',{'api' : api})
    else:
        return render(request,'home.html',{'ticker' : "Enter a ticker symbol above..."})


def about(request):
    return render(request,'about.html',{})

def add_stock(request):
    import requests # Already at top but harmless if repeated
    import json     # Already at top but harmless if repeated

    if request.method == 'POST':
        form = StockForm(request.POST) # No need for 'or None' here
        if form.is_valid():
            form.save()
            messages.success(request, ("Stock has been added!"))
            return redirect('add_stock') # Redirect to the same view to display an empty form
        else:
            # If the form is invalid, re-render the page with errors
            # You need to pass the 'form' object to the template so errors can be displayed
            ticker = Stock.objects.all()
            output=[]

            for ticker_item in ticker:
                # IMPORTANT: Access the actual ticker symbol field, likely .ticker or .symbol
                # If your Stock model has a field named 'ticker'
                symbol_to_fetch = ticker_item.ticker # <--- Corrected this
                # If your Stock model has a field named 'symbol'
                # symbol_to_fetch = ticker_item.symbol # <--- Use this if your field is 'symbol'

                api_request = requests.get("https://financialmodelingprep.com/stable/quote?symbol="+str(symbol_to_fetch)+"&apikey=b5249712421ee83869be287077e59a29")
                try:
                    api = json.loads(api_request.content)
                    # Check if the API returned a list and if it's not empty
                    if api and isinstance(api, list) and len(api) > 0:
                        output.append(api[0]) # Financial Modeling Prep returns a list, take the first item
                    else:
                        # Handle cases where API returns empty list or non-list
                        output.append({'symbol': symbol_to_fetch, 'error': 'No data found for this ticker.'}) # Add symbol for display
                except Exception as e:
                    # Generic catch-all for now, better error handling was in previous suggestions
                    output.append({'symbol': symbol_to_fetch, 'error': 'No data found for this ticker.'}) # Add symbol for display

            # --- CRITICAL FIX: MOVE THIS RETURN STATEMENT OUTSIDE THE LOOP ---
            return render(request, 'add_stock.html', {'ticker': ticker, 'form': form, 'output' : output})
    else:
        # This handles the initial GET request to display an empty form
        form = StockForm() # Create an empty form
        ticker = Stock.objects.all() # Still fetch all tickers if you want to display them on initial load
        output=[] # Initialize output for GET request as well

        for ticker_item in ticker:
            # IMPORTANT: Access the actual ticker symbol field, likely .ticker or .symbol
            symbol_to_fetch = ticker_item.ticker # <--- Corrected this (same as above)

            api_request = requests.get("https://financialmodelingprep.com/stable/quote?symbol="+str(symbol_to_fetch)+"&apikey=b5249712421ee83869be287077e59a29")
            try:
                api = json.loads(api_request.content)
                if api and isinstance(api, list) and len(api) > 0:
                    output.append(api[0])
                else:
                    output.append({'symbol': symbol_to_fetch, 'error': 'No data found for this ticker.'})
            except Exception as e:
                output.append({'symbol': symbol_to_fetch, 'error': 'No data found for this ticker.'})

        return render(request, 'add_stock.html', {'ticker': ticker, 'form': form, 'output': output})

    
def delete(request, stock_id):
    item = Stock.objects.get(pk=stock_id)
    item.delete()
    messages.success(request,'Stock has been deleted!')
    return redirect(delete_stock)

def delete_stock(request):
    ticker = Stock.objects.all()
    return render(request,'delete_stock.html',{ 'ticker' : ticker})
