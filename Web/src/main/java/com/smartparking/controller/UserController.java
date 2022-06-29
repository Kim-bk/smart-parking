package com.smartparking.controller;

import java.util.List;
import java.util.Optional;

import javax.servlet.http.HttpServletRequest;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.ModelAttribute;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.ResponseBody;

import com.smartparking.dto.CustomerDTO;
import com.smartparking.dto.DistrictDTO;
import com.smartparking.dto.ProvinceDTO;
import com.smartparking.dto.WardDTO;
import com.smartparking.entity.CustomerEntity;
import com.smartparking.entity.CustomerParkingEntity;
import com.smartparking.service.impl.CustomerParkingService;
import com.smartparking.service.impl.CustomerService;
import com.smartparking.service.impl.DistrictService;
import com.smartparking.service.impl.ProvinceService;
import com.smartparking.service.impl.WardService;


@Controller
public class UserController {
	
	@Autowired
	private ProvinceService provinceService;
	
	@Autowired
	private DistrictService districtService;
	
	@Autowired
	private WardService wardService;
	
	@Autowired
	private CustomerService customerService;
	
	@Autowired
	private CustomerParkingService cusParService;
	
	
	
	
	
	@GetMapping("/user/home")
	public String getAdminHome(Model model) {
		CustomerDTO customer = new CustomerDTO();
		model.addAttribute("customer",customer);
		List<ProvinceDTO> provinces = provinceService.findAll();
		model.addAttribute("provinces", provinces);
		return "user/index";
	}
	
	@GetMapping("/user/district")
	@ResponseBody
	public List<DistrictDTO> getDistrict(@RequestParam(name="province_id") Optional<String> id){
		if (id.isPresent()) {
			List<DistrictDTO> districts = districtService.findByIdProvince(id.get()); 
			System.out.println(districts.size());
			return districts;
		}
		return null;
	}
	
	@GetMapping("/user/ward")
	@ResponseBody
	public List<WardDTO> getWard(@RequestParam(name="district_id") Optional<String> id){
		if (id.isPresent()) {
			List<WardDTO> wards = wardService.findByDistrict(id.get());
			return wards;
		}
		return null;
	}
	
	@PostMapping(value="/user/add")
	public String addCustomer(@ModelAttribute("customer") CustomerDTO customer) {
		
		customerService.save(customer);
		return "redirect:/user/home";
	}
	
	@PostMapping("/login")
	public String Login(@RequestParam(name="email") Optional<String> email,@RequestParam(name="password") Optional<String> password,HttpServletRequest request,Model model) 
	{
		String email1 = email.get();
		//String pass = password.get();
		if (customerService.findByEmailAndPassword(email1)!=null) {
			CustomerEntity cus = (CustomerEntity) request.getSession().getAttribute("CUSTOMER");
			if (cus == null) {
				cus = new CustomerEntity();
				request.getSession().setAttribute("CUSTOMER", cus);
			}
			cus = customerService.findByEmailAndPassword(email1);
			request.getSession().setAttribute("CUSTOMER", cus);
			model.addAttribute("customer", cus);
			return "user/personal";
		}
		return "redirect:/user/home";
		
	}
	
	@GetMapping("/user/profile")
	public String profile(Model model,HttpServletRequest request) {
		CustomerEntity cus = (CustomerEntity) request.getSession().getAttribute("CUSTOMER");
		model.addAttribute("customer", cus);
		return "user/profile";
		
	}
	
	@GetMapping("/user/statistics")
	public String statistic(Model model,HttpServletRequest request) {
		CustomerEntity cus = (CustomerEntity) request.getSession().getAttribute("CUSTOMER");
		model.addAttribute("customer", cus);
		List<CustomerParkingEntity> list = cusParService.findByCustomer(cus);
		model.addAttribute("list",list);
		float total = 0;
		for (CustomerParkingEntity item : list) {
			total += item.getFee();
		}
		model.addAttribute("total", total);

		return "user/statistic";
		
	}

}
