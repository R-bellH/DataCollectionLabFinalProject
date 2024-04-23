# ~3$ per 1000 requestes <- |compaines|*|job titles| = how many req

# html weight ~= 500kb

# ~10$ per GB of data <- |compaines|*html weight/1000000

companies=500
job_titles=30
html_weight=520 # kb

print("current price for serp : ", 3*companies*job_titles/1000)
print("current price for job search : ", 10*companies*html_weight/1000000)
print("total price : ", 3*companies*job_titles/1000 + 10*companies*html_weight/1000000)

