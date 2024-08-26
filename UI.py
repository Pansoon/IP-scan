import tkinter as tk
from tkinter import messagebox
from IP_address import resolve_domain_to_ip
from PORT_scan import scan_ports
from HTTP_status import get_http_status_code
from aggregation import aggregate_results
from report import generate_report

def run_scan():
    domain = entry_domain.get()
    if not domain:
        messagebox.showwarning("Input Error", "Please enter a domain name.")
        return
    
    try:
        # Step 1: Resolve domain to IP
        ip_address = resolve_domain_to_ip(domain)
        
        # Step 2: Scan ports
        ports = [80, 443, 22]  # You can customize this or make it user-selectable
        port_status = scan_ports(ip_address, ports)
        
        # Step 3: Get HTTP status code
        http_status = get_http_status_code(domain)
        
        # Step 4: Aggregate results
        results = aggregate_results(ip_address, port_status, http_status)
        
        # Step 5: Display results
        display_results(results)
        
        # Step 6: Generate report
        report_type = report_type_var.get()
        generate_report(results, report_type=report_type)
        messagebox.showinfo("Success", f"Report generated as {report_type} format.")
        
    except Exception as e:
        messagebox.showerror("Error", str(e))

def display_results(results):
    result_text = ""
    for key, value in results.items():
        result_text += f"{key}: {value}\n"
    text_results.delete(1.0, tk.END)
    text_results.insert(tk.END, result_text)

# Initialize tkinter window
root = tk.Tk()
root.title("Domain Scanner Tool")

# Domain Entry
tk.Label(root, text="Enter Domain:").grid(row=0, column=0, padx=10, pady=10)
entry_domain = tk.Entry(root, width=50)
entry_domain.grid(row=0, column=1, padx=10, pady=10)

# Report Type Option
report_type_var = tk.StringVar(value='text')
tk.Label(root, text="Report Type:").grid(row=1, column=0, padx=10, pady=10)
tk.Radiobutton(root, text="Text", variable=report_type_var, value='text').grid(row=1, column=1, sticky='w')
tk.Radiobutton(root, text="PDF", variable=report_type_var, value='pdf').grid(row=1, column=1, sticky='e')

# Run Scan Button
tk.Button(root, text="Run Scan", command=run_scan).grid(row=2, column=0, columnspan=2, pady=20)

# Results Display
text_results = tk.Text(root, height=15, width=70)
text_results.grid(row=3, column=0, columnspan=2, padx=10, pady=10)

# Start the GUI event loop
root.mainloop()
