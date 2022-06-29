package com.smartparking.controller;

import java.util.List;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestParam;

import com.smartparking.entity.CustomerEntity;
import com.smartparking.entity.CustomerParkingEntity;
import com.smartparking.service.impl.CustomerParkingService;
import com.smartparking.service.impl.CustomerService;

@Controller
public class AdminController {
	
	@Autowired
	private CustomerParkingService cus_parking_ser;
	
	@Autowired
	private CustomerService customerService;

	@GetMapping("/admin/home")
	public String getAdminHome() {
		return "admin/index";
	}
	
	@GetMapping("/admin/list-member")
	public String getAdminMember(Model model) {
		List<CustomerEntity> list = customerService.findByCustomerCardNot("00000");
		model.addAttribute("list", list);
		return "admin/table";
	}
	
	@GetMapping("/admin/profile")
	public String getProfile() {
		return "admin/profile";
	}
	
	@GetMapping("/admin/statistics")
	public String getStatistics(Model model) {
		List<CustomerParkingEntity> list = cus_parking_ser.findAll();
		model.addAttribute("list", list);
		float total = 0;
		for (CustomerParkingEntity item : list) {
			total += item.getFee();
		}
		model.addAttribute("total", total);

		return "admin/statistic";
	}
	
	@PostMapping("/admin/saveCustomerCard")
	public String saveCard(@RequestParam("customer_id") String id,@RequestParam("customer_card") String card) {
		customerService.update(id, card);
		return "redirect:/admin/home";
	}
	
	
}
