#= Createn By WJM in Sep.7.2020 =#
using LinearAlgebra
#= function sum_string(str_state) #Try to calculate the up-states number.
end =#
function flip(a, i, j)
    f = split(st[a],"")
    if  st[a][i] == '1'
        f[i] = "0"
        f[j] = "1"
        
    else
        f[i] = "1"
        f[j] = "0"
    end
    global b = st_rv[join(f)] 
end

function lable_states(N, st, st_rv)#The N indicate the length of the Heisenbreg
    # st = Dict{Int64, String}()#Here "st" stand for the "states"
    for n in 0:(2^N-1)
        nn = string(n, base = 2, pad = N)#cut extra part
        st[(n+1)] = nn
    end
    # st_rv = Dict{String, Int64}()
    for n in 0:(2^N-1)
        nn = string(n, base = 2, pad = N)#cut extra part
        st_rv[nn] = (n+1)
    end
end

function ()
    
end

global N = 3

println("The length of Heisenbreg chain:", N)
st = Dict{Int64, String}()
st_rv = Dict{String, Int64}()
lable_states(N, st, st_rv)
H = zeros(2^N, 2^N)
for a in 1:2^N
    for i in 1:N
        j = mod1(i+1, N)
        if st[a][i] == st[a][j]
            H[a,a] = H[a,a] + 0.25
        else
            H[a,a] = H[a,a] - 0.25
            flip(a, i, j)
            H[a,b] = 0.5
        end
        # show(stdout, "text/plain", H);println()
    end
end
# show(stdout, "text/plain", H);println()
e_v = eigvals(H)
e_s = eigvecs(H)
show(stdout, "text/plain", e_v);println()
show(stdout, "text/plain", e_s);println()
