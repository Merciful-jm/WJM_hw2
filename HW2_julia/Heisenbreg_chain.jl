#= Createn By WJM in Sep.7.2020 =#
using LinearAlgebra

#= function sum_string(str_state) #Try to calculate the up-states number.

end =#
function flip(a_spin_state, i, j)
    if  i == 1
        i = 0
    else
        i = 1
    end
    if  j == 1
        j = 0
    else
        j = 1
    end
end
function lable_states(N)#The N indicate the length of the Heisenbreg
    states = Dict{Int64, String}()
    for n in 0:(2^N-1)
        nn = string(SubString(bitstring(n),(64+1-N:64)))#cut extra part
        states[n] = nn
    end
end


N = 4
println("The length of Heisenbreg chain:", N)
H = zeros(2^N, 2^N)
for a in 1:2^N
    for i in 1:N
        j = mod1(i+1, N)
        if states[a][i] == states[a][j]
            H[a,a] = H[a,a] + 0.25
        else
            H[a,a] = H[a,a] - 0.25
            b = flip()
        end
    end
end